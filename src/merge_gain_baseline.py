import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def merge_gain_and_baseline():
    """
    Merge gain_long.csv and data_baseline_cleaned.csv, then create yearly data
    """
    print("Loading datasets...")
    
    # Load gain_long.csv
    gain_data = pd.read_csv("notebooks/gain_long.csv")
    gain_data['date'] = pd.to_datetime(gain_data['date'])
    print(f"Gain data loaded: {gain_data.shape}")
    print(f"Countries in gain data: {gain_data['iso3'].nunique()}")
    
    # Load baseline data
    baseline_data = pd.read_csv("data/processed/data_baseline_cleaned.csv")
    baseline_data['date'] = pd.to_datetime(baseline_data['date'])
    print(f"Baseline data loaded: {baseline_data.shape}")
    print(f"Countries in baseline data: {baseline_data['iso3c'].nunique()}")
    
    # Get unique countries from baseline data
    baseline_countries = set(baseline_data['iso3c'].unique())
    print(f"Unique countries in baseline: {len(baseline_countries)}")
    
    # Filter gain data to only include countries in baseline
    gain_filtered = gain_data[gain_data['iso3'].isin(baseline_countries)].copy()
    gain_filtered = gain_filtered.rename(columns={'iso3': 'iso3c'})
    print(f"Gain data after filtering: {gain_filtered.shape}")
    print(f"Countries in filtered gain data: {gain_filtered['iso3c'].nunique()}")
    
    # Merge datasets on country and date
    print("\nMerging datasets...")
    merged_data = pd.merge(baseline_data, gain_filtered, on=['iso3c', 'date'], how='left')
    print(f"Merged data shape: {merged_data.shape}")
    
    # Check for missing GAIN values
    missing_gain = merged_data['GAIN'].isnull().sum()
    print(f"Missing GAIN values: {missing_gain} ({missing_gain/len(merged_data)*100:.1f}%)")
    
    # Create yearly data using averages
    print("\nCreating yearly data...")
    merged_data['year'] = merged_data['date'].dt.year
    
    # Group by country and year, calculate averages for all numeric variables
    yearly_data = merged_data.groupby(['iso3c', 'year']).agg({
        'yield_with_spread': 'mean',
        'sovereign_spread': 'mean',
        'cpi_yoy': 'mean',
        'gdp_annual_growth_rate': 'mean',
        'gdp_per_capita': 'mean',
        'gross gdp': 'mean',
        'debt_to_gdp': 'mean',
        'deficit_to_gdp': 'mean',
        'current_account_balance': 'mean',
        'vulnerability': 'mean',
        'wgi_cc': 'mean',
        'wgi_ge': 'mean',
        'wgi_pv': 'mean',
        'wgi_rl': 'mean',
        'wgi_rq': 'mean',
        'wgi_va': 'mean',
        'GAIN': 'mean'
    }).reset_index()
    
    print(f"Yearly data shape: {yearly_data.shape}")
    
    # Add date column for yearly data (first day of each year)
    yearly_data['date'] = pd.to_datetime(yearly_data['year'].astype(str) + '-01-01')
    
    # Reorder columns to have date first
    cols = ['date', 'iso3c', 'year'] + [col for col in yearly_data.columns if col not in ['date', 'iso3c', 'year']]
    yearly_data = yearly_data[cols]
    
    # Save final dataset
    output_path = "data/processed/data_final.csv"
    yearly_data.to_csv(output_path, index=False)
    print(f"\nFinal dataset saved to: {output_path}")
    
    # Display summary statistics
    print("\n" + "="*80)
    print("FINAL DATASET SUMMARY")
    print("="*80)
    print(f"Shape: {yearly_data.shape}")
    print(f"Countries: {yearly_data['iso3c'].nunique()}")
    print(f"Years: {yearly_data['year'].min()} to {yearly_data['year'].max()}")
    print(f"Variables: {len(yearly_data.columns)}")
    
    # Display sample of final data
    print("\nSample of final dataset:")
    print(yearly_data.head(10))
    
    # Display column names
    print("\nColumns in final dataset:")
    for i, col in enumerate(yearly_data.columns):
        print(f"{i+1:2d}. {col}")
    
    # Check for missing values in final dataset
    print("\nMissing values in final dataset:")
    missing_summary = yearly_data.isnull().sum()
    for col in yearly_data.columns:
        if missing_summary[col] > 0:
            missing_pct = (missing_summary[col] / len(yearly_data)) * 100
            print(f"  {col}: {missing_summary[col]} ({missing_pct:.1f}%)")
    
    return yearly_data

if __name__ == "__main__":
    final_data = merge_gain_and_baseline()
