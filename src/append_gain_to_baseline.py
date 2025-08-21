import pandas as pd
import numpy as np
from pathlib import Path

def append_gain_to_baseline():
    """
    Append gain_filtered.csv to baseline_yearly_aggregated.csv
    Remove country variable and merge on year and iso3c
    """
    # Read the data files
    gain_path = Path("data/processed/gain_filtered.csv")
    baseline_path = Path("data/processed/baseline_yearly_aggregated.csv")
    
    print("Reading gain_filtered.csv...")
    gain_data = pd.read_csv(gain_path)
    
    print("Reading baseline_yearly_aggregated.csv...")
    baseline_data = pd.read_csv(baseline_path)
    
    print(f"Gain data shape: {gain_data.shape}")
    print(f"Baseline data shape: {baseline_data.shape}")
    
    # Remove country variable from both datasets
    gain_data = gain_data.drop('country', axis=1, errors='ignore')
    baseline_data = baseline_data.drop('country', axis=1, errors='ignore')
    
    # Remove date column from gain data (we only need year)
    gain_data = gain_data.drop('date', axis=1, errors='ignore')
    
    print(f"After removing country and date columns:")
    print(f"Gain data shape: {gain_data.shape}")
    print(f"Baseline data shape: {baseline_data.shape}")
    
    # Merge the datasets on year and iso3c
    print("Merging datasets on year and iso3c...")
    merged_data = pd.merge(baseline_data, gain_data, on=['year', 'iso3c'], how='left')
    
    print(f"Merged data shape: {merged_data.shape}")
    
    # Check for missing values in gain column
    missing_gain = merged_data['gain'].isna().sum()
    total_rows = len(merged_data)
    print(f"Missing gain values: {missing_gain} out of {total_rows} rows ({missing_gain/total_rows*100:.1f}%)")
    
    # Check unique countries and years in merged data
    print(f"Unique countries in merged data: {merged_data['iso3c'].nunique()}")
    print(f"Years covered: {merged_data['year'].min()} - {merged_data['year'].max()}")
    
    # Show sample of merged data
    print("\nSample of merged data:")
    print(merged_data[['year', 'iso3c', 'gain', 'yield_with_spread', 'cpi_yoy']].head(10))
    
    # Save merged data
    output_path = Path("data/processed/baseline_with_gain.csv")
    merged_data.to_csv(output_path, index=False)
    print(f"\nSaved merged data to {output_path}")
    
    return merged_data

def main():
    """
    Main function to execute the data appending
    """
    print("Starting gain data appending process...")
    
    # Append gain data to baseline
    merged_data = append_gain_to_baseline()
    
    # Print summary statistics
    print("\n" + "="*50)
    print("FINAL SUMMARY")
    print("="*50)
    print(f"Final merged dataset: {len(merged_data)} rows")
    print(f"Variables in final dataset: {len(merged_data.columns)}")
    print(f"Countries: {merged_data['iso3c'].nunique()}")
    print(f"Years: {merged_data['year'].min()} - {merged_data['year'].max()}")
    
    # Show all column names
    print(f"\nAll variables in final dataset:")
    for i, col in enumerate(merged_data.columns, 1):
        print(f"{i:2d}. {col}")
    
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()
