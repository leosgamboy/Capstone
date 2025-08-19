# Predictive & Causal ML for Climate-Event Risk and Sovereign Bond Impacts

## Project Overview
This project builds an end-to-end system to (1) forecast country-level risk of acute climate events (floods, heatwaves, hurricanes, wildfires) and (2) quantify how those forecasted risks causally affect sovereign bond spreads and default risk.

### Stages
1. **Forecasting Climate-Event Risk**: Data ingestion, feature engineering, and ML modeling to predict event risk and damage.
2. **Causal ML Analysis on Sovereign Bonds**: Merging forecasts with financial data and applying causal inference methods to estimate effects.

## Data Sources
- **EM-DAT**: Country-level disaster events
- **ERA5**: Meteorological features
- **GHSL**: Population exposure
- **Vulnerability Indices**: ND-GAIN, INFORM, Germanwatch
- **Bond Data**: Sovereign yield/CDS spreads
- **Macro Controls**: GDP, debt, inflation, etc.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd Capstone
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Organize data files in the `data/` directory as described above.
4. Use the provided scripts and notebooks in `src/` and `notebooks/` to run the pipeline.

## Outputs
- Forecast model metrics (AUC/RMSE), saved risk-score predictions
- Causal effect estimates (ATEs, heterogeneous effects) with confidence intervals
- Diagnostic plots (ROC curves, event-study graphs, etc.)
