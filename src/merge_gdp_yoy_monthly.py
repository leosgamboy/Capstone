import os
import glob
from datetime import datetime
from typing import List

import pandas as pd

from country_iso_mapping import get_iso_code


INPUT_DIR = "/Users/leosgambato/Documents/GitHub/Capstone/data/external/Data/Control data/GDP_yoy"
OUTPUT_PATH = "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/gdp_annual_growth_rate_monthly.csv"


def list_gdp_files(input_dir: str) -> List[str]:
    pattern = os.path.join(input_dir, "historical_country_*_indicator_GDP_Annual_Growth_Rate.csv")
    return sorted(glob.glob(pattern))


def expand_quarter_to_months(date: pd.Timestamp, value: float) -> pd.DataFrame:
    # Determine the months in the quarter for the given quarter-end date
    quarter = date.to_period("Q")
    month_starts = pd.period_range(start=quarter.start_time.to_period("M"), end=quarter.end_time.to_period("M"), freq="M")
    months = month_starts.to_timestamp(how="start")
    df = pd.DataFrame({
        "date": months.normalize(),
        "gdp_annual_growth_rate": [value] * len(months),
    })
    return df


def process_single_file(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    # Basic normalization
    df = df.rename(columns={
        "Country": "country",
        "Category": "category",
        "DateTime": "datetime",
        "Value": "value",
        "Frequency": "frequency",
        "HistoricalDataSymbol": "historical_symbol",
        "LastUpdate": "last_update",
    })

    # Keep only GDP Annual Growth Rate rows
    df = df[df["category"].str.lower() == "gdp annual growth rate".lower()].copy()

    # Parse datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime", "value"])

    # Map country to ISO3
    df["iso3"] = df["country"].astype(str).str.strip().str.lower().map(get_iso_code)

    # Expand each quarterly observation to three monthly rows within the quarter
    expanded_parts: List[pd.DataFrame] = []
    for _, row in df.iterrows():
        monthly = expand_quarter_to_months(row["datetime"], float(row["value"]))
        monthly.insert(0, "iso3", row["iso3"])  # add iso3 as first column
        expanded_parts.append(monthly)

    if not expanded_parts:
        return pd.DataFrame(columns=["iso3", "date", "gdp_annual_growth_rate"])  # empty

    out = pd.concat(expanded_parts, ignore_index=True)

    # Filter to 1980-01 through 2025-12
    start_date = pd.Timestamp("1980-01-01")
    end_date = pd.Timestamp("2025-12-31")
    out = out[(out["date"] >= start_date) & (out["date"] <= end_date)]

    return out[["iso3", "date", "gdp_annual_growth_rate"]]


def main():
    files = list_gdp_files(INPUT_DIR)
    all_parts: List[pd.DataFrame] = []
    for fp in files:
        all_parts.append(process_single_file(fp))

    if not all_parts:
        print("No input files found or no data extracted.")
        return

    merged = pd.concat(all_parts, ignore_index=True)

    # Drop potential duplicates (e.g., if source provides overlapping revisions)
    merged = merged.drop_duplicates(subset=["iso3", "date"]).sort_values(["iso3", "date"]).reset_index(drop=True)

    # Ensure date is date-only string (no time)
    merged["date"] = merged["date"].dt.date.astype(str)

    # Write output (long format: iso3, date, gdp_annual_growth_rate)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    merged.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(merged):,} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


