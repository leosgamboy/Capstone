import os
import glob
from typing import List

import pandas as pd

from country_iso_mapping import get_iso_code


INPUT_DIR = "/Users/leosgambato/Documents/GitHub/Capstone/data/external/Data/Control data/ratings"
OUTPUT_PATH = "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/ratings_combined.csv"


def list_rating_files(input_dir: str) -> List[str]:
    pattern = os.path.join(input_dir, "ratings_historical_*_.csv")
    return sorted(glob.glob(pattern))


def process_single_file(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df.rename(columns={
        "Country": "country",
        "Date": "date",
        "Agency": "agency",
        "Rating": "rating",
        "Outlook": "outlook",
    })

    # Parse date to date-only
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df = df.dropna(subset=["date"]).copy()

    # ISO3 mapping
    df["iso3"] = df["country"].astype(str).str.strip().str.lower().map(get_iso_code)

    # Filter date range 1980-2025
    start = pd.to_datetime("1980-01-01").date()
    end = pd.to_datetime("2025-12-31").date()
    df = df[(df["date"] >= start) & (df["date"] <= end)].copy()

    # Keep long-format essential columns
    return df[["iso3", "date", "agency", "rating", "outlook"]]


def main():
    files = list_rating_files(INPUT_DIR)
    parts: List[pd.DataFrame] = []
    for fp in files:
        parts.append(process_single_file(fp))

    if not parts:
        print("No rating files found.")
        return

    out = pd.concat(parts, ignore_index=True)
    out = out.sort_values(["iso3", "date", "agency"]).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(out):,} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


