#!/usr/bin/env python3
"""
Process yield data files to create cleaned, monthly aggregated datasets with spreads.
"""

import pandas as pd
import numpy as np
import re
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import glob

# Configuration
YIELD_DATA_DIR = "data/external/Data/Control data/Yield data/Yield data real "
OUTPUT_DIR = "data/processed"

# ISO3 code extraction regex and override mapping
ISO3_PATTERN = re.compile(r'IG([A-Z]{3})')

# Override mapping for any odd cases
ISO3_OVERRIDE = {
    'EUF0210DEU': 'EUR',  # Euro area
    'EUF0110DEU': 'EUR',  # Euro area
    'EUF0010DEU': 'EUR',  # Euro area
    'EUF0310DEU': 'EUR',  # Euro area
    'US-10yearbond-constand-GFD': 'USA',  # Alternative US file
}

def extract_iso3_from_filename(filename):
    """Extract ISO3 country code from filename."""
    # Remove file extension
    name = Path(filename).stem
    
    # Check override first
    if name in ISO3_OVERRIDE:
        return ISO3_OVERRIDE[name]
    
    # Try regex pattern
    match = ISO3_PATTERN.search(name)
    if match:
        return match.group(1)
    
    # If no match, return None
    return None

def process_yield_file(file_path):
    """Process a single yield data file."""
    try:
        # Read the file as text first to find the data section
        with open(file_path, 'r') as f:
            lines = f.readlines()
            
        # Extract ISO3 from filename
        filename = os.path.basename(file_path)
        iso3 = extract_iso3_from_filename(filename)
        
        if iso3 is None:
            print(f"Warning: Could not extract ISO3 from {filename}")
            return None
        
        # Find the data section (look for "Date,Ticker,Open,High,Low,Close")
        data_start_idx = None
        for i, line in enumerate(lines):
            if 'Date,Ticker,Open,High,Low,Close' in line:
                data_start_idx = i
                break
        
        if data_start_idx is None:
            print(f"Warning: Could not find data section in {filename}")
            return None
        
        # Extract the data lines
        data_lines = lines[data_start_idx + 1:]
        
        # Parse the data
        data_rows = []
        for line in data_lines:
            line = line.strip()
            if line and ',' in line:
                parts = line.split(',')
                if len(parts) >= 6:
                    # Only include rows where Close value is not empty
                    if parts[5].strip() and parts[5].strip() != '':
                        data_rows.append(parts[:6])
        
        if not data_rows:
            print(f"Warning: No valid data rows found in {filename}")
            return None
        
        # Create DataFrame
        data_df = pd.DataFrame(data_rows, columns=['Date', 'Ticker', 'Open', 'High', 'Low', 'Close'])
        
        # Clean up the data
        data_df['Date'] = pd.to_datetime(data_df['Date'], errors='coerce')
        data_df['Close'] = pd.to_numeric(data_df['Close'], errors='coerce')
        
        # Remove rows with invalid dates or yields
        data_df = data_df.dropna(subset=['Date', 'Close'])
        
        # Filter to reasonable date range (1980 onwards for modern sovereign bond markets)
        data_df = data_df[data_df['Date'] >= '1980-01-01']
        
        if len(data_df) == 0:
            print(f"Warning: No data after 1980 in {filename}")
            return None
        
        # Create result DataFrame
        result_df = pd.DataFrame({
            'date': data_df['Date'],
            'yield': data_df['Close'],
            'iso3': iso3
        })
        
        # Ensure proper data types
        result_df['yield'] = pd.to_numeric(result_df['yield'], errors='coerce')
        result_df['iso3'] = result_df['iso3'].astype(str)
        
        # Remove any remaining NaN values
        result_df = result_df.dropna(subset=['yield'])
        
        if len(result_df) == 0:
            print(f"Warning: No valid yield data found in {filename}")
            return None
        
        # Set date as index for resampling
        result_df = result_df.set_index('date')
        
        # Resample to monthly (month start) and take mean
        # Only resample numeric columns
        monthly_df = result_df[['yield']].resample('MS').mean()
        
        # Add iso3 column back (take first value for each month)
        monthly_df['iso3'] = result_df['iso3'].resample('MS').first()
        
        # Reset index to get date as column
        monthly_df = monthly_df.reset_index()
        
        # Remove any remaining NaN values after resampling
        monthly_df = monthly_df.dropna()
        
        if len(monthly_df) == 0:
            print(f"Warning: No valid monthly data after resampling in {filename}")
            return None
        
        print(f"Processed {filename}: {len(monthly_df)} monthly observations for {iso3}")
        return monthly_df
        
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return None

def process_all_yield_files():
    """Process all yield data files and combine them."""
    # Get all CSV files in the yield data directory
    csv_files = glob.glob(os.path.join(YIELD_DATA_DIR, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {YIELD_DATA_DIR}")
        return None
    
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Process each file
    all_data = []
    for file_path in csv_files:
        result = process_yield_file(file_path)
        if result is not None:
            all_data.append(result)
    
    if not all_data:
        print("No data was successfully processed from any files")
        return None
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates and sort
    combined_df = combined_df.drop_duplicates(subset=['date', 'iso3']).sort_values(['iso3', 'date'])
    
    # Final data quality check
    print(f"\nTotal processed data: {len(combined_df)} observations across {combined_df['iso3'].nunique()} countries")
    print(f"Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
    
    return combined_df

def compute_spreads(yields_df):
    """Compute spreads relative to US yields."""
    print("\nComputing spreads relative to US yields...")
    
    # Extract US yields
    us_yields = yields_df[yields_df['iso3'] == 'USA'].copy()
    if len(us_yields) == 0:
        print("Warning: No US yield data found")
        return None
    
    us_yields = us_yields[['date', 'yield']].rename(columns={'yield': 'us_yield'})
    
    # Merge US yields back to main dataset
    yields_with_us = yields_df.merge(us_yields, on='date', how='left')
    
    # Compute spread
    yields_with_us['spread'] = yields_with_us['yield'] - yields_with_us['us_yield']
    
    # Remove US rows (spread is always 0)
    spreads_df = yields_with_us[yields_with_us['iso3'] != 'USA'].copy()
    
    # Keep only necessary columns
    spreads_df = spreads_df[['date', 'iso3', 'yield', 'spread']].reset_index(drop=True)
    
    print(f"Computed spreads for {len(spreads_df)} observations across {spreads_df['iso3'].nunique()} countries")
    
    return spreads_df

def perform_qa_checks(yields_df, spreads_df):
    """Perform quality assurance checks."""
    print("\nPerforming QA checks...")
    
    # Check 1: No duplicates on (iso3, date)
    duplicates = yields_df.duplicated(subset=['iso3', 'date']).sum()
    if duplicates > 0:
        print(f"WARNING: Found {duplicates} duplicate (iso3, date) combinations in yields data")
    else:
        print("✓ No duplicates on (iso3, date) in yields data")
    
    # Check 2: USA absent from spreads dataset
    usa_in_spreads = 'USA' in spreads_df['iso3'].values
    if usa_in_spreads:
        print("WARNING: USA found in spreads dataset")
    else:
        print("✓ USA absent from spreads dataset")
    
    # Check 3: Verify spread calculation for a random country
    non_usa_countries = yields_df[yields_df['iso3'] != 'USA']['iso3'].unique()
    if len(non_usa_countries) > 0:
        test_country = np.random.choice(non_usa_countries)
        print(f"\nTesting spread calculation for {test_country}:")
        
        # Get recent data for the test country
        test_data = spreads_df[spreads_df['iso3'] == test_country].tail(3)
        
        for _, row in test_data.iterrows():
            # Reconstruct the calculation
            us_yield = yields_df[(yields_df['iso3'] == 'USA') & (yields_df['date'] == row['date'])]['yield'].iloc[0]
            expected_spread = row['yield'] - us_yield
            actual_spread = row['spread']
            
            if abs(expected_spread - actual_spread) < 1e-10:
                print(f"  ✓ {row['date'].strftime('%Y-%m')}: {row['yield']:.3f} - {us_yield:.3f} = {actual_spread:.3f}")
            else:
                print(f"  ✗ {row['date'].strftime('%Y-%m')}: {row['yield']:.3f} - {us_yield:.3f} = {expected_spread:.3f} (got {actual_spread:.3f})")

def save_outputs(yields_df, spreads_df):
    """Save the processed data to CSV files."""
    # Create output directory if it doesn't exist
    output_path = Path(OUTPUT_DIR)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save yields data
    yields_file = output_path / "sovereign_yields_monthly.csv"
    yields_df.to_csv(yields_file, index=False)
    print(f"\nSaved yields data to: {yields_file}")
    
    # Save spreads data
    spreads_file = output_path / "sovereign_spreads_monthly.csv"
    spreads_df.to_csv(spreads_file, index=False)
    print(f"Saved spreads data to: {spreads_file}")
    
    # Print summary statistics
    print(f"\nSummary statistics:")
    print(f"Yields data: {len(yields_df)} observations, {yields_df['iso3'].nunique()} countries")
    print(f"Spreads data: {len(spreads_df)} observations, {spreads_df['iso3'].nunique()} countries")
    print(f"Date range: {yields_df['date'].min()} to {yields_df['date'].max()}")
    
    # Print some sample countries
    sample_countries = yields_df['iso3'].value_counts().head(10)
    print(f"\nTop 10 countries by number of observations:")
    for country, count in sample_countries.items():
        print(f"  {country}: {count}")

def main():
    """Main processing pipeline."""
    print("Starting yield data processing pipeline...")
    
    # Step 1: Process all yield files
    yields_df = process_all_yield_files()
    if yields_df is None:
        print("Failed to process yield files")
        return
    
    # Step 2: Compute spreads
    spreads_df = compute_spreads(yields_df)
    if spreads_df is None:
        print("Failed to compute spreads")
        return
    
    # Step 3: Perform QA checks
    perform_qa_checks(yields_df, spreads_df)
    
    # Step 4: Save outputs
    save_outputs(yields_df, spreads_df)
    
    print("\nYield data processing completed successfully!")

if __name__ == "__main__":
    main()
