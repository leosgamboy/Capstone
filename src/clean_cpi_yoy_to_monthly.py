import os
import re
from typing import List

import pandas as pd

from country_iso_mapping import COUNTRY_ISO_MAPPING


INPUT_PATH = "/Users/leosgambato/Documents/GitHub/Capstone/data/external/Data/Control data/IMF CPI data.csv"
OUTPUT_PATH = "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/cpi_cleaned.csv"


def select_quarter_columns(columns: List[str]) -> List[str]:
    quarter_cols: List[str] = []
    for col in columns:
        if re.match(r"^\d{4}-Q[1-4]$", col):
            year = int(col[:4])
            if 1990 <= year <= 2025:
                quarter_cols.append(col)
    return quarter_cols


def is_headline_row(row: pd.Series) -> bool:
    series_code = str(row.get("SERIES_CODE", ""))
    # Accept headline CPI by series code indicators: CP00 (All items) or _T (Total)
    return (".CP00." in series_code) or (".CPI._T." in series_code)


def main() -> None:
    # Read the wide CPI file (contains monthly and quarterly series for many COICOP groups)
    df = pd.read_csv(INPUT_PATH, low_memory=False)

    # Identify quarterly columns in the desired window
    quarter_cols = select_quarter_columns(list(df.columns))
    if not quarter_cols:
        raise RuntimeError("No quarterly columns found in 1990–2025 range.")

    # Filter: headline CPI only, YOY, Quarterly frequency, and countries present in mapping
    df = df[
        df.apply(is_headline_row, axis=1)
        & df["TYPE_OF_TRANSFORMATION"].astype(str).str.contains("YOY", case=False, na=False)
        & df["FREQUENCY"].astype(str).str.lower().eq("quarterly")
    ].copy()

    # Keep only the necessary columns
    keep_cols = ["SERIES_CODE"] + quarter_cols
    df = df[keep_cols].copy()

    # Extract ISO3 from SERIES_CODE (first 3 chars before the first dot)
    df["iso3"] = df["SERIES_CODE"].astype(str).str.split(".").str[0].str.upper()

    # Filter to allowed ISO3s based on our mapping values
    allowed_iso3 = set(COUNTRY_ISO_MAPPING.values())
    df = df[df["iso3"].isin(allowed_iso3)].copy()

    # Melt to long format by quarter
    long_df = df.melt(
        id_vars=["iso3"],
        value_vars=quarter_cols,
        var_name="quarter",
        value_name="cpi_yoy",
    )

    # Drop empty and non-numeric values
    long_df["cpi_yoy"] = pd.to_numeric(long_df["cpi_yoy"], errors="coerce")
    long_df = long_df.dropna(subset=["cpi_yoy"]).reset_index(drop=True)

    # Expand each quarter to 3 months with the same CPI YoY value
    records = []
    for _, r in long_df.iterrows():
        year = int(r["quarter"][:4])
        q = int(r["quarter"][6])  # last char of 'Qx'
        first_month = (q - 1) * 3 + 1
        for m in range(first_month, first_month + 3):
            date_str = f"{year}-{m:02d}-01"
            records.append((r["iso3"], date_str, float(r["cpi_yoy"])) )

    out = pd.DataFrame(records, columns=["iso3", "Date", "CPI YoY"])

    # Filter by date range
    out["Date"] = pd.to_datetime(out["Date"]).dt.date.astype(str)
    out = out[(out["Date"] >= "1990-01-01") & (out["Date"] <= "2025-12-31")]

    # Sort and deduplicate
    out = out.drop_duplicates(subset=["iso3", "Date"]).sort_values(["iso3", "Date"]).reset_index(drop=True)

    # Write
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(out):,} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


