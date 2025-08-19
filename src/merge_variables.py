import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_data():
    """
    Load and clean all data files, standardizing country codes and dates
    """
    data_dir = Path("data/processed")
    
    # Load sovereign yields (likely dependent variable)
    print("Loading sovereign yields...")
    yields = pd.read_csv(data_dir / "sovereign_yields_monthly.csv")
    yields['date'] = pd.to_datetime(yields['date'])
    yields = yields.rename(columns={'iso3': 'iso3c', 'yield': 'sovereign_yield'})
    
    # Load sovereign spreads (likely dependent variable)
    print("Loading sovereign spreads...")
    spreads = pd.read_csv(data_dir / "sovereign_spreads_monthly.csv")
    spreads['date'] = pd.to_datetime(spreads['date'])
    spreads = spreads.rename(columns={'iso3': 'iso3c', 'yield': 'yield_with_spread', 'spread': 'sovereign_spread'})
    
    # Load CPI data
    print("Loading CPI data...")
    cpi = pd.read_csv(data_dir / "cpi_cleaned.csv")
    cpi['Date'] = pd.to_datetime(cpi['Date'])
    cpi = cpi.rename(columns={'Date': 'date', 'iso3': 'iso3c', 'CPI YoY': 'cpi_yoy'})
    
    # Load GDP growth rate
    print("Loading GDP growth rate...")
    gdp_growth = pd.read_csv(data_dir / "gdp_annual_growth_rate_monthly.csv")
    gdp_growth['date'] = pd.to_datetime(gdp_growth['date'])
    gdp_growth = gdp_growth.rename(columns={'iso3': 'iso3c'})
    
    # Load GDP per capita
    print("Loading GDP per capita...")
    gdp_pc = pd.read_csv(data_dir / "gdp_per_capita_monthly.csv")
    gdp_pc['Date'] = pd.to_datetime(gdp_pc['Date'])
    gdp_pc = gdp_pc.rename(columns={'iso3': 'iso3c', 'Date': 'date'})
    
    # Load debt to GDP
    print("Loading debt to GDP...")
    debt_gdp = pd.read_csv(data_dir / "debt_to_gdp_monthly.csv")
    debt_gdp['Date'] = pd.to_datetime(debt_gdp['Date'])
    debt_gdp = debt_gdp.rename(columns={'iso3': 'iso3c', 'Date': 'date', 'debt-to-gdp': 'debt_to_gdp'})
    
    # Load deficit to GDP
    print("Loading deficit to GDP...")
    deficit_gdp = pd.read_csv(data_dir / "deficit_to_gdp_monthly.csv")
    deficit_gdp['Date'] = pd.to_datetime(deficit_gdp['Date'])
    deficit_gdp = deficit_gdp.rename(columns={'iso3': 'iso3c', 'Date': 'date', 'deficit-to-gdp': 'deficit_to_gdp'})
    
    # Load current account balance
    print("Loading current account balance...")
    cab = pd.read_csv(data_dir / "current_account_balance_monthly.csv")
    cab['Date'] = pd.to_datetime(cab['Date'])
    cab = cab.rename(columns={'iso3': 'iso3c', 'Date': 'date', 'account balance': 'current_account_balance'})
    
    # Load NEER (Nominal Effective Exchange Rate)
    print("Loading NEER...")
    neer = pd.read_csv(data_dir / "neer_monthly.csv")
    neer['Date'] = pd.to_datetime(neer['Date'])
    neer = neer.rename(columns={'Date': 'date', 'iso3': 'iso3c'})
    
    # Load vulnerability index
    print("Loading vulnerability index...")
    vulnerability = pd.read_csv(data_dir / "vulnerability_monthly.csv")
    vulnerability['Date'] = pd.to_datetime(vulnerability['Date'])
    vulnerability = vulnerability.rename(columns={'Date': 'date', 'iso3': 'iso3c'})
    
    # Load WGI (Worldwide Governance Indicators)
    print("Loading WGI data...")
    wgi = pd.read_csv(data_dir / "wgi_cleaned.csv")
    wgi['date'] = pd.to_datetime(wgi['date'])
    wgi = wgi.rename(columns={'iso3c': 'iso3c'})
    
    # Load ratings data
    print("Loading ratings data...")
    ratings = pd.read_csv(data_dir / "ratings_monthly_panel.csv")
    ratings['Date'] = pd.to_datetime(ratings['Date'])
    ratings = ratings.rename(columns={'Date': 'date', 'Country': 'iso3c'})
    
    return {
        'yields': yields,
        'spreads': spreads,
        'cpi': cpi,
        'gdp_growth': gdp_growth,
        'gdp_pc': gdp_pc,
        'debt_gdp': debt_gdp,
        'deficit_gdp': deficit_gdp,
        'cab': cab,
        'neer': neer,
        'vulnerability': vulnerability,
        'wgi': wgi,
        'ratings': ratings
    }

def merge_all_variables(data_dict):
    """
    Merge all variables on country code (iso3c) and date
    """
    print("\nStarting merge process...")
    
    # Start with yields as the base (likely the main dependent variable)
    merged = data_dict['yields'].copy()
    print(f"Base dataset (yields): {merged.shape}")
    
    # Merge spreads
    merged = pd.merge(merged, data_dict['spreads'][['iso3c', 'date', 'sovereign_spread']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging spreads: {merged.shape}")
    
    # Merge CPI
    merged = pd.merge(merged, data_dict['cpi'][['iso3c', 'date', 'cpi_yoy']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging CPI: {merged.shape}")
    
    # Merge GDP growth
    merged = pd.merge(merged, data_dict['gdp_growth'][['iso3c', 'date', 'gdp_annual_growth_rate']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging GDP growth: {merged.shape}")
    
    # Merge GDP per capita
    merged = pd.merge(merged, data_dict['gdp_pc'][['iso3c', 'date', 'gdp_per_capita']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging GDP per capita: {merged.shape}")
    
    # Merge debt to GDP
    merged = pd.merge(merged, data_dict['debt_gdp'][['iso3c', 'date', 'debt_to_gdp']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging debt to GDP: {merged.shape}")
    
    # Merge deficit to GDP
    merged = pd.merge(merged, data_dict['deficit_gdp'][['iso3c', 'date', 'deficit_to_gdp']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging deficit to GDP: {merged.shape}")
    
    # Merge current account balance
    merged = pd.merge(merged, data_dict['cab'][['iso3c', 'date', 'current_account_balance']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging current account balance: {merged.shape}")
    
    # Merge NEER
    merged = pd.merge(merged, data_dict['neer'][['iso3c', 'date', 'NEER']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging NEER: {merged.shape}")
    
    # Merge vulnerability
    merged = pd.merge(merged, data_dict['vulnerability'][['iso3c', 'date', 'vulnerability']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging vulnerability: {merged.shape}")
    
    # Merge WGI indicators
    wgi_cols = ['iso3c', 'date', 'wgi_cc', 'wgi_ge', 'wgi_pv', 'wgi_rl', 'wgi_rq', 'wgi_va']
    merged = pd.merge(merged, data_dict['wgi'][wgi_cols], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging WGI: {merged.shape}")
    
    # Merge ratings
    ratings_cols = ['iso3c', 'date', 'Rating_Fitch', 'Outlook_Fitch', 'Rating_S&P', 
                   'Outlook_S&P', 'Rating_DBRS', 'Outlook_DBRS', 'Rating_Moody\'s', 'Outlook_Moody\'s']
    merged = pd.merge(merged, data_dict['ratings'][ratings_cols], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging ratings: {merged.shape}")
    
    return merged

def analyze_missing_data(merged_data):
    """
    Analyze missing data by country and variable
    """
    print("\n" + "="*80)
    print("MISSING DATA ANALYSIS BY COUNTRY")
    print("="*80)
    
    # Get unique countries
    countries = merged_data['iso3c'].unique()
    
    # Variables to check (excluding iso3c and date)
    variables = [col for col in merged_data.columns if col not in ['iso3c', 'date']]
    
    # Create missing data summary
    missing_summary = []
    
    for country in sorted(countries):
        country_data = merged_data[merged_data['iso3c'] == country]
        total_obs = len(country_data)
        
        if total_obs == 0:
            continue
            
        country_summary = {'Country': country, 'Total_Observations': total_obs}
        
        for var in variables:
            missing_count = country_data[var].isna().sum()
            missing_pct = (missing_count / total_obs) * 100
            country_summary[f'{var}_missing'] = missing_count
            country_summary[f'{var}_missing_pct'] = round(missing_pct, 1)
        
        missing_summary.append(country_summary)
    
    # Convert to DataFrame
    missing_df = pd.DataFrame(missing_summary)
    
    # Display summary statistics
    print(f"\nTotal countries: {len(countries)}")
    print(f"Total variables: {len(variables)}")
    print(f"Total observations: {len(merged_data)}")
    
    # Show countries with most complete data
    print("\n" + "="*80)
    print("COUNTRIES WITH MOST COMPLETE DATA (Top 10)")
    print("="*80)
    
    # Calculate overall completeness for each country
    completeness_cols = [col for col in missing_df.columns if col.endswith('_missing_pct')]
    missing_df['overall_completeness'] = 100 - missing_df[completeness_cols].mean(axis=1)
    
    top_complete = missing_df.nlargest(10, 'overall_completeness')[['Country', 'Total_Observations', 'overall_completeness']]
    print(top_complete.round(1))
    
    # Show countries with least complete data
    print("\n" + "="*80)
    print("COUNTRIES WITH LEAST COMPLETE DATA (Bottom 10)")
    print("="*80)
    bottom_complete = missing_df.nsmallest(10, 'overall_completeness')[['Country', 'Total_Observations', 'overall_completeness']]
    print(bottom_complete.round(1))
    
    # Show variable completeness
    print("\n" + "="*80)
    print("VARIABLE COMPLETENESS ACROSS ALL COUNTRIES")
    print("="*80)
    
    var_completeness = []
    for var in variables:
        missing_total = merged_data[var].isna().sum()
        missing_pct = (missing_total / len(merged_data)) * 100
        var_completeness.append({
            'Variable': var,
            'Missing_Count': missing_total,
            'Missing_Percentage': round(missing_pct, 1),
            'Complete_Percentage': round(100 - missing_pct, 1)
        })
    
    var_df = pd.DataFrame(var_completeness)
    var_df = var_df.sort_values('Complete_Percentage', ascending=False)
    print(var_df)
    
    return missing_df, var_df

def main():
    """
    Main function to execute the merge and analysis
    """
    print("Loading and merging all variables...")
    
    # Load all data
    data_dict = load_and_clean_data()
    
    # Merge all variables
    merged_data = merge_all_variables(data_dict)
    
    # Save merged dataset
    output_path = "data/processed/merged_all_variables.csv"
    merged_data.to_csv(output_path, index=False)
    print(f"\nMerged dataset saved to: {output_path}")
    print(f"Final dataset shape: {merged_data.shape}")
    
    # Analyze missing data
    missing_by_country, missing_by_variable = analyze_missing_data(merged_data)
    
    # Save missing data analysis
    missing_by_country.to_csv("data/processed/missing_data_by_country.csv", index=False)
    missing_by_variable.to_csv("data/processed/missing_data_by_variable.csv", index=False)
    print(f"\nMissing data analysis saved to:")
    print(f"  - data/processed/missing_data_by_country.csv")
    print(f"  - data/processed/missing_data_by_variable.csv")
    
    # Display sample of merged data
    print("\n" + "="*80)
    print("SAMPLE OF MERGED DATASET")
    print("="*80)
    print(merged_data.head(10))
    
    print("\n" + "="*80)
    print("COLUMN NAMES IN MERGED DATASET")
    print("="*80)
    for i, col in enumerate(merged_data.columns):
        print(f"{i+1:2d}. {col}")

if __name__ == "__main__":
    main()
