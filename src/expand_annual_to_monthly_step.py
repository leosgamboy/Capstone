import os
from typing import List, Tuple

import pandas as pd


INPUTS = [
    ("/Users/leosgambato/Documents/GitHub/Capstone/data/processed/current_account_balance_cleaned.csv", "account balance", "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/current_account_balance_monthly.csv"),
    ("/Users/leosgambato/Documents/GitHub/Capstone/data/processed/debt_to_gdp_cleaned.csv", "debt-to-gdp", "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/debt_to_gdp_monthly.csv"),
    ("/Users/leosgambato/Documents/GitHub/Capstone/data/processed/deficit_to_gdp_cleaned.csv", "deficit-to-gdp", "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/deficit_to_gdp_monthly.csv"),
    ("/Users/leosgambato/Documents/GitHub/Capstone/data/processed/gdp_per_capita_cleaned.csv", "gdp_per_capita", "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/gdp_per_capita_monthly.csv"),
    ("/Users/leosgambato/Documents/GitHub/Capstone/data/processed/gdp_gross_cleaned.csv", "gross gdp", "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/gdp_gross_monthly.csv"),
]


def expand_to_months(df: pd.DataFrame, value_col: str) -> pd.DataFrame:
    df = df.copy()
    # Expect Date as YYYY-MM-DD with month=01 for annual
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"])  # keep only valid dates

    records: List[Tuple[str, str, float]] = []
    for iso3, date, val in df[["iso3", "Date", value_col]].itertuples(index=False):
        year = date.year
        for month in range(1, 13):
            month_date = pd.Timestamp(year=year, month=month, day=1)
            records.append((iso3, month_date.date().isoformat(), float(val)))

    out = pd.DataFrame(records, columns=["iso3", "Date", value_col])

    # Filter to 1990-01-01 through 2025-12-01 just in case
    out = out[(out["Date"] >= "1990-01-01") & (out["Date"] <= "2025-12-01")]
    return out.sort_values(["iso3", "Date"]).reset_index(drop=True)


def main() -> None:
    for in_path, value_col, out_path in INPUTS:
        df = pd.read_csv(in_path)
        out = expand_to_months(df, value_col)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        out.to_csv(out_path, index=False)
        print(f"Wrote {len(out):,} rows to {out_path}")


if __name__ == "__main__":
    main()


