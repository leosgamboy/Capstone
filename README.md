# DML of Climate-Event Risk and Sovereign Bond Impacts

## Project Overview
This project's goal is to quantify how climate risks causally affect sovereign bond spreads and default risk.

### Stages
1. **Forecasting Climate-Event Risk**: Data ingestion, feature engineering, and ML modeling to predict event risk and damage.
2. **Causal ML Analysis on Sovereign Bonds**: Merging forecasts with financial data and applying causal inference methods to estimate effects.

## Main Data Sources
Data 
- **EM-DAT**: Country-level disaster events
- **Vulnerability Indices**: ND-GAIN, accessible here: https://gain.nd.edu/
- **Bond Data**, can be accessed through Refinitiv LSEG workspace: Sovereign yield/CDS
- **Macro Controls** WEO database: GDP, debt, inflation, etc. Accessible here: https://www.imf.org/en/Publications/WEO/weo-database/2025/april
- ** Country


3. Organize data files in the `data/` directory as described above.
4. Use the provided scripts and notebooks in `src/` and `notebooks/` to run the pipeline.


