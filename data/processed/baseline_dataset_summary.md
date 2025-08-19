

Baseline Dataset Summary

## Overview
This document summarizes the baseline dataset created from the "Variables real for study" folder, containing the core variables for the sovereign bond analysis project.

## Dataset Information
- **Total observations**: 63,338
- **Total countries**: 80
- **Total variables**: 16
- **Time period**: 2009-2025 (monthly frequency)
- **File size**: ~11.3 MB
- **Output file**: `data_baseline_cleaned.csv`

## Variables Included

### Dependent Variables
1. **yield_with_spread** - Sovereign bond yields with spread information
2. **sovereign_spread** - Sovereign bond spreads over risk-free rate

### Control Variables

#### Macroeconomic Indicators
3. **cpi_yoy** - Consumer Price Index (year-over-year change)
4. **gdp_annual_growth_rate** - GDP annual growth rate
5. **gdp_per_capita** - GDP per capita
6. **gross gdp** - Gross GDP values
7. **debt_to_gdp** - Government debt as percentage of GDP
8. **deficit_to_gdp** - Government deficit as percentage of GDP
9. **current_account_balance** - Current account balance

#### Climate & Governance Indicators
10. **vulnerability** - Climate vulnerability index
11. **wgi_cc** - Control of Corruption (Worldwide Governance Indicators)
12. **wgi_ge** - Government Effectiveness
13. **wgi_pv** - Political Stability and Absence of Violence
14. **wgi_rl** - Rule of Law
15. **wgi_rq** - Regulatory Quality
16. **wgi_va** - Voice and Accountability

## Data Quality Analysis

### Overall Completeness by Country
- **Top performers**: Malta (88.5%), Latvia (88.3%), Slovakia (87.7%), Russia (87.6%), Lithuania (87.4%)
- **Bottom performers**: Ethiopia (7.5%), Saudi Arabia (9.7%), Kuwait (10.4%), Uruguay (10.7%), UAE (10.8%)

### Variable Completeness
- **Most complete**: Deficit to GDP (88.3%), GDP per capita (88.2%), Gross GDP (88.2%)
- **Least complete**: WGI indicators (64.5% for all governance indicators), CPI YoY (67.3%)

### Key Insights

#### 1. Regional Performance
- **Eastern Europe**: Generally high data quality (Slovakia, Latvia, Lithuania, Russia)
- **Western Europe**: Good coverage (Malta, Cyprus, Slovenia)
- **Emerging markets**: Variable coverage, with some showing surprisingly good quality
- **Middle East**: Lower coverage (UAE, Saudi Arabia, Kuwait)

#### 2. Variable Group Performance
- **Macroeconomic variables**: Generally well-covered (80-88% completeness)
- **Financial variables**: Moderate coverage (70-88% completeness)
- **Governance indicators**: Consistent but lower coverage (64.5% across all WGI indicators)
- **Climate vulnerability**: Moderate coverage (72.4%)

#### 3. Sample Characteristics
- **Developed markets**: Generally good coverage but not uniformly high
- **Emerging markets**: More variable, with some showing excellent coverage
- **Smaller economies**: Often have better data quality than expected

## Comparison with Previous Dataset

### Key Differences:
- **Smaller size**: 63,338 vs 71,822 observations
- **Fewer variables**: 16 vs 24 variables
- **Focused scope**: Core variables only, no credit ratings
- **Better quality**: Higher overall completeness for included variables
- **Cleaner structure**: More focused on essential variables for analysis

### Advantages of Baseline Dataset:
- **Focused analysis**: Contains only the most relevant variables
- **Better quality**: Higher completeness for core variables
- **Cleaner structure**: Easier to work with for initial analysis
- **Consistent coverage**: More uniform data availability across countries

## Recommendations for Analysis

### 1. Sample Selection
- **Primary analysis**: Focus on countries with >80% overall completeness
- **Secondary analysis**: Include countries with >70% completeness
- **Robustness checks**: Use countries with >60% completeness

### 2. Variable Usage
- **Core analysis**: Use variables with >80% completeness (most macroeconomic indicators)
- **Extended analysis**: Include governance indicators where available (64.5% completeness)
- **Climate analysis**: Use vulnerability index (72.4% completeness)

### 3. Missing Data Strategy
- **Imputation**: Consider multiple imputation for countries with moderate missing data
- **Fixed effects**: Use country-fixed effects to control for unobserved heterogeneity
- **Sample selection**: Focus on countries with better data coverage for initial analysis

## Files Generated
1. **data_baseline_cleaned.csv** - Main baseline dataset
2. **baseline_missing_data_by_country.csv** - Missing data analysis by country
3. **baseline_missing_data_by_variable.csv** - Missing data analysis by variable

## Next Steps
1. **Initial analysis**: Use baseline dataset for preliminary model specification
2. **Sample refinement**: Select countries based on completeness requirements
3. **Variable transformation**: Create derived variables and lags as needed
4. **Model development**: Design models considering data availability constraints
5. **Robustness checks**: Compare results with different sample compositions

## Usage Notes
- **Primary file**: `data_baseline_cleaned.csv`
- **Country codes**: All standardized to 3-letter ISO codes
- **Date format**: YYYY-MM-DD (monthly frequency)
- **Missing values**: Represented as NaN
- **Variable names**: Standardized and descriptive



