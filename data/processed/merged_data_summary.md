# Merged Dataset Summary

## Overview
This document summarizes the merged dataset containing all dependent and control variables for the sovereign bond analysis project.

## Dataset Information
- **Total observations**: 71,822
- **Total countries**: 90
- **Total variables**: 24
- **Time period**: 1980-2025 (monthly frequency)
- **File size**: ~13.4 MB

## Variables Included

### Dependent Variables (Likely)
1. **sovereign_yield** - Sovereign bond yields
2. **sovereign_spread** - Sovereign bond spreads over risk-free rate

### Control Variables

#### Macroeconomic Indicators
3. **cpi_yoy** - Consumer Price Index (year-over-year change)
4. **gdp_annual_growth_rate** - GDP annual growth rate
5. **gdp_per_capita** - GDP per capita
6. **debt_to_gdp** - Government debt as percentage of GDP
7. **deficit_to_gdp** - Government deficit as percentage of GDP
8. **current_account_balance** - Current account balance

#### Financial & External Indicators
9. **NEER** - Nominal Effective Exchange Rate
10. **vulnerability** - Climate vulnerability index

#### Governance Indicators (Worldwide Governance Indicators - WGI)
11. **wgi_cc** - Control of Corruption
12. **wgi_ge** - Government Effectiveness
13. **wgi_pv** - Political Stability and Absence of Violence
14. **wgi_rl** - Rule of Law
15. **wgi_rq** - Regulatory Quality
16. **wgi_va** - Voice and Accountability

#### Credit Ratings
17. **Rating_Fitch** - Fitch credit rating
18. **Outlook_Fitch** - Fitch rating outlook
19. **Rating_S&P** - Standard & Poor's credit rating
20. **Outlook_S&P** - S&P rating outlook
21. **Rating_DBRS** - DBRS credit rating
22. **Outlook_DBRS** - DBRS rating outlook
23. **Rating_Moody's** - Moody's credit rating
24. **Outlook_Moody's** - Moody's rating outlook

## Data Quality Analysis

### Overall Completeness by Country
- **Top performers**: Canada (78.7%), Netherlands (76.9%), Germany (76.5%)
- **Bottom performers**: Estonia, Ethiopia, Ghana, Morocco, Ukraine, UAE, Uruguay (all 4.2%)

### Variable Completeness
- **Most complete**: GDP growth rate (70.1%), GDP per capita (68.4%), deficit to GDP (68.4%)
- **Least complete**: DBRS ratings (15.3%), Outlook DBRS (15.2%), Fitch outlook (45.4%)

### Key Insights

#### 1. Developed vs. Emerging Markets
- **Developed countries** (Canada, Netherlands, Germany, Switzerland, Japan) show consistently high data completeness (75-79%)
- **Emerging markets** show more variable coverage, with some countries having very low completeness

#### 2. Variable Group Performance
- **Macroeconomic variables**: Generally well-covered across most countries
- **Financial variables**: High coverage in developed markets, variable in emerging markets
- **Governance indicators**: Better coverage in emerging markets (some African and Asian countries show 70-80% completeness)
- **Credit ratings**: Highly variable coverage, with DBRS showing the lowest coverage globally

#### 3. Regional Patterns
- **Europe**: Generally high data quality and completeness
- **North America**: Excellent coverage
- **Asia-Pacific**: Variable coverage, with Japan and Korea showing high completeness
- **Latin America**: Moderate coverage, with Argentina showing relatively good completeness
- **Africa**: Variable coverage, with some countries showing surprisingly good governance data coverage

## Recommendations for Analysis

### 1. Sample Selection
- Focus on countries with >70% overall completeness for comprehensive analysis
- Consider separate analyses for developed vs. emerging markets
- Use countries with >80% completeness for specific variable groups when needed

### 2. Variable Usage
- **Primary analysis**: Use variables with >60% completeness (most macroeconomic and financial indicators)
- **Secondary analysis**: Use governance indicators where available (50% completeness)
- **Limited use**: DBRS ratings due to very low coverage (15%)

### 3. Missing Data Handling
- Consider multiple imputation for countries with moderate missing data
- Use country-fixed effects to control for unobserved heterogeneity
- Implement robustness checks using different sample compositions

## Files Generated
1. **merged_all_variables.csv** - Complete merged dataset
2. **missing_data_by_country.csv** - Detailed missing data analysis by country
3. **missing_data_table_clean.csv** - Clean missing data table
4. **missing_data_table_enhanced.csv** - Enhanced table with variable group completeness
5. **variable_completeness_summary.csv** - Summary of variable completeness
6. **missing_data_heatmap_top20.csv** - Heatmap-style table for top 20 countries

## Next Steps
1. **Data cleaning**: Address any data quality issues identified
2. **Sample selection**: Choose countries based on completeness requirements
3. **Missing data strategy**: Implement appropriate imputation or selection methods
4. **Variable transformation**: Create derived variables and lags as needed
5. **Model specification**: Design models considering data availability constraints



