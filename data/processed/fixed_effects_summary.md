# Fixed Effects and Lagged Variables Summary

## Overview
This document summarizes the fixed effects and lagged variables that were added to the baseline dataset for the sovereign bond analysis.

## Dataset Transformation

### Original Dataset
- **File**: `data_baseline_cleaned.csv`
- **Observations**: 63,338
- **Countries**: 80
- **Variables**: 16

### Final Dataset (After Adding Fixed Effects and Lags)
- **Observations**: 63,338 (unchanged)
- **Countries**: 80 (unchanged)
- **Variables**: 653 (increased by 637)

## Fixed Effects Added

### 1. Country Fixed Effects
- **Type**: Dummy variables for each country
- **Count**: 80 country dummies
- **Naming convention**: `country_ISO3C` (e.g., `country_USA`, `country_DEU`)
- **Purpose**: Control for unobserved time-invariant country characteristics
- **Usage**: Include in regression models to control for country-specific effects

### 2. Time Fixed Effects
- **Type**: Dummy variables for each year-month combination
- **Count**: 552 time dummies
- **Naming convention**: `time_YYYY-MM` (e.g., `time_2020-01`, `time_2020-02`)
- **Purpose**: Control for global time-varying factors affecting all countries
- **Usage**: Include in regression models to control for time-specific effects

## Lagged Variables Added

### 1. Sovereign Spread Lags
- **`sovereign_spread_lag1`**: One-period lag of sovereign spread (y(t-1))
- **`sovereign_spread_lag2`**: Two-period lag of sovereign spread (y(t-2))
- **Purpose**: Capture persistence and dynamics in sovereign spreads
- **Usage**: Include in dynamic panel models to control for autocorrelation

## Variable Structure

### Core Variables (Original 16)
1. **date** - Date of observation
2. **iso3c** - Country code
3. **yield_with_spread** - Sovereign bond yields
4. **sovereign_spread** - Sovereign bond spreads
5. **cpi_yoy** - Consumer Price Index (year-over-year)
6. **gdp_annual_growth_rate** - GDP growth rate
7. **gdp_per_capita** - GDP per capita
8. **gross gdp** - Gross GDP values
9. **debt_to_gdp** - Government debt to GDP ratio
10. **deficit_to_gdp** - Government deficit to GDP ratio
11. **current_account_balance** - Current account balance
12. **vulnerability** - Climate vulnerability index
13. **wgi_cc** - Control of Corruption
14. **wgi_ge** - Government Effectiveness
15. **wgi_pv** - Political Stability
16. **wgi_rl** - Rule of Law
17. **wgi_rq** - Regulatory Quality
18. **wgi_va** - Voice and Accountability

### Fixed Effects Variables (632)
- **Country dummies**: 80 variables
- **Time dummies**: 552 variables

### Lagged Variables (2)
- **sovereign_spread_lag1**: 1-period lag
- **sovereign_spread_lag2**: 2-period lag

## Data Quality

### Missing Values Summary
- **Most complete variables**: Deficit to GDP (88.3%), GDP per capita (88.2%), Gross GDP (88.2%)
- **Least complete variables**: WGI indicators (64.5%), CPI YoY (67.3%)
- **Lagged variables**: 
  - `sovereign_spread_lag1`: 18,410 missing (29.1%)
  - `sovereign_spread_lag2`: 18,412 missing (29.1%)

### Data Types
- **Boolean**: 632 variables (fixed effects dummies)
- **Float64**: 18 variables (original continuous variables)
- **Datetime64**: 1 variable (date)
- **Object**: 1 variable (iso3c)
- **Period**: 1 variable (year_month)

## Usage in Analysis

### 1. Basic Fixed Effects Model
```python
# Example regression with country and time fixed effects
import statsmodels.api as sm

# Select variables for regression
X = df_data[['cpi_yoy', 'gdp_annual_growth_rate', 'debt_to_gdp', 'vulnerability'] + 
           [col for col in df_data.columns if col.startswith('country_')] +
           [col for col in df_data.columns if col.startswith('time_')]]

y = df_data['sovereign_spread']

# Fit model
model = sm.OLS(y, X)
results = model.fit()
```

### 2. Dynamic Panel Model with Lags
```python
# Example with lagged dependent variable
X_dynamic = df_data[['sovereign_spread_lag1', 'cpi_yoy', 'gdp_annual_growth_rate', 'debt_to_gdp', 'vulnerability'] + 
                   [col for col in df_data.columns if col.startswith('country_')] +
                   [col for col in df_data.columns if col.startswith('time_')]]

y_dynamic = df_data['sovereign_spread']

# Fit dynamic model
model_dynamic = sm.OLS(y_dynamic, X_dynamic)
results_dynamic = model_dynamic.fit()
```

## Benefits

### 1. **Country Fixed Effects**
- Control for unobserved country-specific factors
- Account for institutional differences
- Reduce omitted variable bias

### 2. **Time Fixed Effects**
- Control for global shocks and trends
- Account for common time-varying factors
- Control for business cycle effects

### 3. **Lagged Variables**
- Capture persistence in sovereign spreads
- Control for autocorrelation
- Enable dynamic analysis

## Files Generated

1. **`data_baseline_cleaned.csv`** - Original baseline dataset
2. **`01_data_cleaning.ipynb`** - Jupyter notebook with fixed effects code
3. **`create_fixed_effects.py`** - Standalone Python script
4. **`fixed_effects_summary.md`** - This summary document

## Next Steps

1. **Model specification**: Use the fixed effects in regression models
2. **Sample selection**: Consider dropping observations with missing lagged variables
3. **Robustness checks**: Test different fixed effects specifications
4. **Dynamic analysis**: Explore the lagged variable relationships
5. **Model diagnostics**: Check for multicollinearity and other issues

## Notes

- **Memory usage**: The dataset is now significantly larger due to dummy variables
- **Multicollinearity**: Be aware of perfect multicollinearity when using all fixed effects
- **Missing data**: Consider strategies for handling missing values in lagged variables
- **Computational efficiency**: Large number of variables may require efficient estimation methods



