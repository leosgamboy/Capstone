import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def load_and_clean_baseline_data():
    """
    Load and clean all data files from the Variables real for study folder
    """
    data_dir = Path("data/processed/Variables real for study")
    
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
    gdp_pc = gdp_pc.rename(columns={'Date': 'date', 'iso3': 'iso3c'})
    
    # Load GDP gross
    print("Loading GDP gross...")
    gdp_gross = pd.read_csv(data_dir / "gdp_gross_monthly.csv")
    gdp_gross['Date'] = pd.to_datetime(gdp_gross['Date'])
    gdp_gross = gdp_gross.rename(columns={'Date': 'date', 'iso3': 'iso3c'})
    
    # Load debt to GDP
    print("Loading debt to GDP...")
    debt_gdp = pd.read_csv(data_dir / "debt_to_gdp_monthly.csv")
    debt_gdp['Date'] = pd.to_datetime(debt_gdp['Date'])
    debt_gdp = debt_gdp.rename(columns={'Date': 'date', 'iso3': 'iso3c', 'debt-to-gdp': 'debt_to_gdp'})
    
    # Load deficit to GDP
    print("Loading deficit to GDP...")
    deficit_gdp = pd.read_csv(data_dir / "deficit_to_gdp_monthly.csv")
    deficit_gdp['Date'] = pd.to_datetime(deficit_gdp['Date'])
    deficit_gdp = deficit_gdp.rename(columns={'Date': 'date', 'iso3': 'iso3c', 'deficit-to-gdp': 'deficit_to_gdp'})
    
    # Load current account balance
    print("Loading current account balance...")
    cab = pd.read_csv(data_dir / "current_account_balance_monthly.csv")
    cab['Date'] = pd.to_datetime(cab['Date'])
    cab = cab.rename(columns={'Date': 'date', 'iso3': 'iso3c', 'account balance': 'current_account_balance'})
    
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
    
    return {
        'spreads': spreads,
        'cpi': cpi,
        'gdp_growth': gdp_growth,
        'gdp_pc': gdp_pc,
        'gdp_gross': gdp_gross,
        'debt_gdp': debt_gdp,
        'deficit_gdp': deficit_gdp,
        'cab': cab,
        'vulnerability': vulnerability,
        'wgi': wgi
    }

def fix_country_codes_baseline(data_dict):
    """
    Fix country names to use proper 3-letter ISO codes
    """
    print("\nFixing country codes...")
    
    # Define the country name mappings
    country_mappings = {
        'ESTONIA': 'EST',
        'ETHIOPIA': 'ETH', 
        'IVORY COAST': 'CIV',
        'GHANA': 'GHA',
        'KUWAIT': 'KWT',
        'MOROCCO': 'MAR',
        'SAUDI ARABIA': 'SAU',
        'UKRAINE': 'UKR',
        'UNITED ARAB EMIRATES': 'ARE',
        'URUGUAY': 'URY'
    }
    
    # Apply mappings to all datasets
    for name, dataset in data_dict.items():
        if 'iso3c' in dataset.columns:
            for old_name, new_code in country_mappings.items():
                if old_name in dataset['iso3c'].values:
                    count = len(dataset[dataset['iso3c'] == old_name])
                    dataset['iso3c'] = dataset['iso3c'].replace(old_name, new_code)
                    print(f"  {name}: {old_name} -> {new_code} ({count} observations)")
    
    return data_dict

def merge_all_baseline_variables(data_dict):
    """
    Merge all variables on country code (iso3c) and date
    """
    print("\nStarting merge process...")
    
    # Start with spreads as the base (likely the main dependent variable)
    merged = data_dict['spreads'].copy()
    print(f"Base dataset (spreads): {merged.shape}")
    
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
    
    # Merge GDP gross
    merged = pd.merge(merged, data_dict['gdp_gross'][['iso3c', 'date', 'gross gdp']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging GDP gross: {merged.shape}")
    
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
    
    # Merge vulnerability
    merged = pd.merge(merged, data_dict['vulnerability'][['iso3c', 'date', 'vulnerability']], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging vulnerability: {merged.shape}")
    
    # Merge WGI indicators
    wgi_cols = ['iso3c', 'date', 'wgi_cc', 'wgi_ge', 'wgi_pv', 'wgi_rl', 'wgi_rq', 'wgi_va']
    merged = pd.merge(merged, data_dict['wgi'][wgi_cols], 
                      on=['iso3c', 'date'], how='outer')
    print(f"After merging WGI: {merged.shape}")
    
    return merged

def analyze_missing_data_baseline(merged_data):
    """
    Analyze missing data by country and variable for the baseline dataset
    """
    print("\n" + "="*80)
    print("MISSING DATA ANALYSIS BY COUNTRY - BASELINE DATASET")
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
    print("COUNTRIES WITH MOST COMPLETE DATA (Top 15)")
    print("="*80)
    
    # Calculate overall completeness for each country
    completeness_cols = [col for col in missing_df.columns if col.endswith('_missing_pct')]
    missing_df['overall_completeness'] = 100 - missing_df[completeness_cols].mean(axis=1)
    
    top_complete = missing_df.nlargest(15, 'overall_completeness')[['Country', 'Total_Observations', 'overall_completeness']]
    print(top_complete.round(1))
    
    # Show countries with least complete data
    print("\n" + "="*80)
    print("COUNTRIES WITH LEAST COMPLETE DATA (Bottom 15)")
    print("="*80)
    bottom_complete = missing_df.nsmallest(15, 'overall_completeness')[['Country', 'Total_Observations', 'overall_completeness']]
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
    Main function to execute the baseline merge and analysis
    """
    print("Loading and merging baseline variables...")
    
    # Load all data
    data_dict = load_and_clean_baseline_data()
    
    # Fix country codes
    data_dict = fix_country_codes_baseline(data_dict)
    
    # Merge all variables
    merged_data = merge_all_baseline_variables(data_dict)
    
    # Save merged dataset
    output_path = "data/processed/data_baseline_cleaned.csv"
    merged_data.to_csv(output_path, index=False)
    print(f"\nBaseline dataset saved to: {output_path}")
    print(f"Final dataset shape: {merged_data.shape}")
    
    # Analyze missing data
    missing_by_country, missing_by_variable = analyze_missing_data_baseline(merged_data)
    
    # Save missing data analysis
    missing_by_country.to_csv("data/processed/baseline_missing_data_by_country.csv", index=False)
    missing_by_variable.to_csv("data/processed/baseline_missing_data_by_variable.csv", index=False)
    print(f"\nMissing data analysis saved to:")
    print(f"  - data/processed/baseline_missing_data_by_country.csv")
    print(f"  - data/processed/baseline_missing_data_by_variable.csv")
    
    # Display sample of merged data
    print("\n" + "="*80)
    print("SAMPLE OF BASELINE DATASET")
    print("="*80)
    print(merged_data.head(10))
    
    print("\n" + "="*80)
    print("COLUMN NAMES IN BASELINE DATASET")
    print("="*80)
    for i, col in enumerate(merged_data.columns):
        print(f"{i+1:2d}. {col}")
    
    return merged_data

if __name__ == "__main__":
    main()




