import os
import re
from typing import List, Tuple

import pandas as pd


DATA_DIR = "/Users/leosgambato/Documents/GitHub/Capstone/data/external/Data/Control data/IMF data"
OUTPUT_DIR = "/Users/leosgambato/Documents/GitHub/Capstone/data/processed"


def get_allowed_iso3_from_sovereign_yields(sovereign_yields_path: str) -> List[str]:
    df = pd.read_csv(sovereign_yields_path)
    iso3 = sorted(df["iso3"].unique())
    return iso3


def select_year_columns(columns: List[str], start_year: int = 1990, end_year: int = 2025) -> List[str]:
    year_cols: List[str] = []
    for col in columns:
        if re.fullmatch(r"\d{4}", str(col)):
            year = int(col)
            if start_year <= year <= end_year:
                year_cols.append(col)
    return year_cols


def clean_wide_file(input_path: str, value_var_name: str, output_filename: str, require_annual: bool = True) -> Tuple[str, int]:
    df = pd.read_csv(input_path, low_memory=False)

    year_cols = select_year_columns(list(df.columns))
    if not year_cols:
        raise RuntimeError(f"No year columns found in {input_path}")

    # Filter to Annual frequency where available
    if require_annual and "FREQUENCY" in df.columns:
        df = df[df["FREQUENCY"].astype(str).str.lower().eq("annual")].copy()

    # Extract ISO3 from SERIES_CODE prefix
    if "SERIES_CODE" not in df.columns:
        raise RuntimeError(f"SERIES_CODE column not found in {input_path}")
    df["iso3"] = df["SERIES_CODE"].astype(str).str.split(".").str[0].str.upper()

    # Restrict to the sovereign yields country coverage
    allowed_iso3 = set(get_allowed_iso3_from_sovereign_yields(os.path.join(OUTPUT_DIR, "sovereign_yields_monthly.csv")))
    df = df[df["iso3"].isin(allowed_iso3)].copy()

    # Melt to long format
    long_df = df.melt(id_vars=["iso3"], value_vars=year_cols, var_name="year", value_name=value_var_name)

    # Drop NA and coerce to numeric
    long_df[value_var_name] = pd.to_numeric(long_df[value_var_name], errors="coerce")
    long_df = long_df.dropna(subset=[value_var_name]).copy()

    # Build Date and sort
    long_df["Date"] = pd.to_datetime(long_df["year"].astype(int).astype(str) + "-01-01").dt.date.astype(str)
    long_df = long_df.drop(columns=["year"]).sort_values(["iso3", "Date"]).reset_index(drop=True)

    # Reorder columns
    long_df = long_df[["iso3", "Date", value_var_name]]

    # Write output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)
    long_df.to_csv(output_path, index=False)
    return output_path, len(long_df)


def main():
    tasks = [
        (os.path.join(DATA_DIR, "current_account_balance.csv"), "account balance", "current_account_balance_cleaned.csv"),
        (os.path.join(DATA_DIR, "data_debt_percentage_gdp.csv"), "debt-to-gdp", "debt_to_gdp_cleaned.csv"),
        (os.path.join(DATA_DIR, "data_deficit_percentage_gdp.csv"), "deficit-to-gdp", "deficit_to_gdp_cleaned.csv"),
        (os.path.join(DATA_DIR, "data_gdp_gross.csv"), "gross gdp", "gdp_gross_cleaned.csv"),
        (os.path.join(DATA_DIR, "data_gdp_per_capita_usd.csv"), "gdp_per_capita", "gdp_per_capita_cleaned.csv"),
    ]

    for input_path, var_name, out_name in tasks:
        output_path, n = clean_wide_file(input_path, var_name, out_name, require_annual=True)
        print(f"Wrote {n:,} rows to {output_path}")


if __name__ == "__main__":
    main()


