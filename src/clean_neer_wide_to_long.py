import os
import re
from typing import Dict, List

import pandas as pd


INPUT_PATH = "/Users/leosgambato/Documents/GitHub/Capstone/data/external/Data/Control data/IMF data/NEER.csv"
OUTPUT_PATH = "/Users/leosgambato/Documents/GitHub/Capstone/data/processed/neer_monthly.csv"


# Minimal ISO alpha-2 to alpha-3 mapping for countries present in sovereign_yields_monthly.csv
ALPHA2_TO_ISO3: Dict[str, str] = {
    "AR": "ARG", "AM": "ARM", "AU": "AUS", "AT": "AUT", "BE": "BEL", "BD": "BGD", 
    "BG": "BGR", "BR": "BRA", "BW": "BWA", "CA": "CAN", "CH": "CHE", "CL": "CHL", 
    "CN": "CHN", "CI": "CIV", "CO": "COL", "HR": "HRV", "CY": "CYP", "CZ": "CZE", 
    "DK": "DNK", "EG": "EGY", "ES": "ESP", "FI": "FIN", "FR": "FRA", "DE": "DEU", 
    "GR": "GRC", "HK": "HKG", "HU": "HUN", "IS": "ISL", "IN": "IND", "ID": "IDN", 
    "IE": "IRL", "IL": "ISR", "IT": "ITA", "JP": "JPN", "KE": "KEN", "KR": "KOR", 
    "LK": "LKA", "LT": "LTU", "LU": "LUX", "LV": "LVA", "MY": "MYS", "MT": "MLT", 
    "MX": "MEX", "NA": "NAM", "NG": "NGA", "NL": "NLD", "NO": "NOR", "NZ": "NZL", 
    "PK": "PAK", "PE": "PER", "PH": "PHL", "PL": "POL", "PT": "PRT", "QA": "QAT", 
    "RO": "ROU", "RU": "RUS", "RS": "SRB", "SG": "SGP", "SK": "SVK", "SI": "SVN", 
    "ZA": "ZAF", "SE": "SWE", "TH": "THA", "TR": "TUR", "TW": "TWN", "UG": "UGA", 
    "GB": "GBR", "US": "USA", "VN": "VNM", "ZM": "ZMB"
}


def parse_date_yyyymm(s: str) -> str:
    m = re.match(r"^(\d{4})M(\d{2})$", str(s))
    if not m:
        return None
    year, month = m.groups()
    return f"{year}-{month}-01"


def main() -> None:
    # Read as strings to preserve formatting, then clean
    df = pd.read_csv(INPUT_PATH, dtype=str)

    # Identify NEER columns and corresponding alpha-2 codes
    neer_cols: List[str] = [c for c in df.columns if c.startswith("NEER_")]
    col_to_a2: Dict[str, str] = {}
    for c in neer_cols:
        suffix = c.split("_")[-1]
        if len(suffix) == 2 and suffix.isalpha():
            col_to_a2[c] = suffix
        # skip aggregates like EA12 or unknown codes

    # Reshape to long
    long_df = df.melt(id_vars=["Date"], value_vars=list(col_to_a2.keys()), var_name="col", value_name="NEER")

    # Map to ISO3
    long_df["a2"] = long_df["col"].map(col_to_a2)
    long_df["iso3"] = long_df["a2"].map(ALPHA2_TO_ISO3)
    long_df = long_df.dropna(subset=["iso3"]).copy()

    # Clean numeric values: remove thousands separators and convert
    long_df["NEER"] = (
        long_df["NEER"].astype(str).str.replace(",", "", regex=False).str.replace("\"", "", regex=False)
    )
    long_df["NEER"] = pd.to_numeric(long_df["NEER"], errors="coerce")
    long_df = long_df.dropna(subset=["NEER"]).copy()

    # Standardize Date
    long_df["Date"] = long_df["Date"].apply(parse_date_yyyymm)
    long_df = long_df.dropna(subset=["Date"]).copy()

    out = long_df[["iso3", "Date", "NEER"]].sort_values(["iso3", "Date"]).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    out.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(out):,} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()


