import pandas as pd
import numpy as np
import os
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import glob
from country_iso_mapping import get_iso_code

def parse_date(date_str):
    """Parse date string in various formats"""
    try:
        # Try different date formats
        for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%d/%m/%Y']:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except:
                continue
        # If specific formats fail, try pandas default parsing
        return pd.to_datetime(date_str)
    except:
        return None

def create_monthly_panel(start_date='1980-01-01', end_date='2025-12-31'):
    """Create monthly date range from start_date to end_date"""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    
    # Create monthly date range
    dates = pd.date_range(start=start, end=end, freq='MS')  # Month Start
    return dates

def process_ratings_file(file_path):
    """Process a single ratings CSV file"""
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Extract country name from filename and convert to ISO code
        country_name = os.path.basename(file_path).replace('ratings_historical_', '').replace('_.csv', '').replace('_', ' ')
        country_iso = get_iso_code(country_name)
        
        # Parse dates
        df['Date'] = df['Date'].apply(parse_date)
        
        # Remove rows with invalid dates
        df = df.dropna(subset=['Date'])
        
        # Sort by date (most recent first, as per the data structure)
        df = df.sort_values('Date', ascending=False)
        
        # Keep only the most recent rating for each agency at each date
        # This handles cases where multiple agencies update on the same date
        df = df.drop_duplicates(subset=['Date', 'Agency'], keep='first')
        
        return df, country_iso
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def create_rating_series(df, country, monthly_dates):
    """Create monthly rating series for a country"""
    if df is None or df.empty:
        return None
    
    # Create a DataFrame with all monthly dates
    monthly_df = pd.DataFrame({'Date': monthly_dates})
    
    # For each agency, create the rating series
    agencies = df['Agency'].unique()
    
    for agency in agencies:
        agency_data = df[df['Agency'] == agency].copy()
        
        if agency_data.empty:
            continue
            
        # Sort by date (oldest first for forward fill)
        agency_data = agency_data.sort_values('Date')
        
        # Convert rating dates to month start dates for proper matching
        agency_data['MonthStart'] = agency_data['Date'].dt.to_period('M').dt.start_time
        
        # Create a temporary DataFrame with all dates
        temp_df = pd.DataFrame({'Date': monthly_dates})
        temp_df['MonthStart'] = temp_df['Date'].dt.to_period('M').dt.start_time
        
        # Merge with agency data using month start dates
        temp_df = temp_df.merge(agency_data[['MonthStart', 'Rating', 'Outlook']], 
                               on='MonthStart', how='left')
        
        # Forward fill the ratings (ratings remain constant until next update)
        temp_df['Rating'] = temp_df['Rating'].ffill()
        temp_df['Outlook'] = temp_df['Outlook'].ffill()
        
        # Add agency suffix to column names
        temp_df[f'Rating_{agency}'] = temp_df['Rating']
        temp_df[f'Outlook_{agency}'] = temp_df['Outlook']
        
        # Merge back to monthly_df
        monthly_df = monthly_df.merge(temp_df[['Date', f'Rating_{agency}', f'Outlook_{agency}']], 
                                     on='Date', how='left')
    
    # Add country column
    monthly_df['Country'] = country
    
    return monthly_df

def main():
    """Main function to process all ratings data"""
    
    # Define paths
    ratings_dir = 'data/external/Data/Control data/ratings'
    output_file = 'data/processed/ratings_monthly_panel.csv'
    
    # Create monthly date range
    monthly_dates = create_monthly_panel()
    print(f"Created monthly date range from {monthly_dates[0]} to {monthly_dates[-1]}")
    
    # Get all CSV files in the ratings directory
    csv_files = glob.glob(os.path.join(ratings_dir, '*.csv'))
    print(f"Found {len(csv_files)} CSV files to process")
    
    # Process each file
    all_data = []
    
    for file_path in csv_files:
        print(f"Processing {os.path.basename(file_path)}...")
        
        # Process the file
        df, country = process_ratings_file(file_path)
        
        if df is not None and not df.empty:
            # Create monthly rating series
            monthly_series = create_rating_series(df, country, monthly_dates)
            
            if monthly_series is not None:
                all_data.append(monthly_series)
                print(f"  - Processed {country}: {len(df)} rating updates")
            else:
                print(f"  - Failed to create series for {country}")
        else:
            print(f"  - No valid data found in {file_path}")
    
    # Combine all data
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Reorder columns
        country_col = combined_df.pop('Country')
        date_col = combined_df.pop('Date')
        combined_df.insert(0, 'Date', date_col)
        combined_df.insert(1, 'Country', country_col)
        
        # Save to CSV
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        combined_df.to_csv(output_file, index=False)
        
        print(f"\nProcessing complete!")
        print(f"Output saved to: {output_file}")
        print(f"Shape: {combined_df.shape}")
        print(f"Countries: {combined_df['Country'].nunique()}")
        print(f"Date range: {combined_df['Date'].min()} to {combined_df['Date'].max()}")
        
        # Show sample of the data
        print("\nSample of processed data:")
        print(combined_df.head(10))
        
        # Show summary statistics
        print("\nSummary by country:")
        for country in combined_df['Country'].unique():
            country_data = combined_df[combined_df['Country'] == country]
            rating_cols = [col for col in country_data.columns if col.startswith('Rating_')]
            non_null_ratings = country_data[rating_cols].notna().any(axis=1).sum()
            print(f"  {country}: {non_null_ratings} months with ratings out of {len(country_data)} total months")
            
    else:
        print("No data was processed successfully!")

if __name__ == "__main__":
    main() 