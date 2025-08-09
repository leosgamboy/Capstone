#!/usr/bin/env python3
"""
Run WGI integration and provide comprehensive data summary
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class WGICleaner:
    def __init__(self):
        self.wgi_file = "data/external/Data/Control data/wgidataset_excel/wgidataset.xlsx"
        self.output_file = "data/processed/wgi_cleaned.csv"
        
        # Target countries (73 countries from bond yield data)
        self.target_countries = [
            'USA', 'DEU', 'JPN', 'GBR', 'FRA', 'ITA', 'CAN', 'AUS', 'ESP', 'NLD', 
            'BEL', 'AUT', 'CHE', 'SWE', 'NOR', 'DNK', 'FIN', 'IRL', 'PRT', 'GRC', 
            'POL', 'CZE', 'HUN', 'SVK', 'SVN', 'EST', 'LVA', 'LTU', 'BGR', 'ROU', 
            'HRV', 'CYP', 'MLT', 'LUX', 'ISL', 'RUS', 'UKR', 'MEX', 'KOR', 'CHN', 
            'IND', 'IDN', 'MYS', 'THA', 'PHL', 'VNM', 'SGP', 'HKG', 'TWN', 'TUR', 
            'ISR', 'SAU', 'ARE', 'QAT', 'KWT', 'EGY', 'MAR', 'NGA', 'KEN', 'GHA', 
            'ETH', 'ZAF', 'BRA', 'ARG', 'CHL', 'COL', 'PER', 'URY', 'NZL'
        ]
        
        # WGI indicators we want
        self.target_indicators = ['cc', 'ge', 'rq', 'rl', 'va', 'pv']
    
    def load_wgi_data(self):
        """Load the WGI Excel file"""
        print("📊 Loading WGI data...")
        try:
            wgi_data = pd.read_excel(self.wgi_file)
            print(f"  ✅ Loaded {len(wgi_data):,} rows")
            print(f"   Columns: {list(wgi_data.columns)}")
            return wgi_data
        except Exception as e:
            print(f"  ❌ Error: {e}")
            return None
    
    def clean_and_filter_wgi(self, wgi_data):
        """Clean and filter WGI data"""
        print("\n🔧 Cleaning and filtering WGI data...")
        
        # Filter for target countries
        filtered_data = wgi_data[wgi_data['code'].isin(self.target_countries)].copy()
        print(f"   Filtered to target countries: {len(filtered_data):,} rows")
        
        # Filter for target indicators
        filtered_data = filtered_data[filtered_data['indicator'].isin(self.target_indicators)].copy()
        print(f"   Filtered to target indicators: {len(filtered_data):,} rows")
        
        # Remove rows with missing estimates
        filtered_data = filtered_data[filtered_data['estimate'].notna()].copy()
        print(f"  ✅ Removed missing estimates: {len(filtered_data):,} rows")
        
        # Check coverage by indicator
        print(f"\n📊 Coverage by indicator:")
        for indicator in self.target_indicators:
            indicator_data = filtered_data[filtered_data['indicator'] == indicator]
            countries = indicator_data['code'].nunique()
            years = indicator_data['year'].nunique()
            print(f"  {indicator}: {countries} countries, {years} years ({len(indicator_data):,} obs)")
        
        return filtered_data
    
    def reshape_to_wide_format(self, wgi_data):
        """Reshape from long to wide format"""
        print("\n🔄 Reshaping to wide format...")
        
        # Pivot the data to wide format
        wide_data = wgi_data.pivot_table(
            index=['code', 'year'],
            columns='indicator',
            values='estimate',
            aggfunc='first'
        ).reset_index()
        
        # Rename columns to add wgi_ prefix
        wide_data.columns = ['iso3c', 'year'] + [f'wgi_{col}' for col in wide_data.columns[2:]]
        
        print(f"  ✅ Reshaped data shape: {wide_data.shape}")
        print(f"  📋 Columns: {list(wide_data.columns)}")
        
        return wide_data
    
    def create_monthly_panel(self, wgi_data):
        """Convert annual data to monthly panel"""
        print("\n🔄 Creating monthly panel...")
        
        # Convert year to datetime
        wgi_data['date'] = pd.to_datetime(wgi_data['year'].astype(str) + '-01-01')
        
        # Create monthly frequency
        monthly_data = []
        
        for _, row in wgi_data.iterrows():
            # Create 12 monthly observations for each year
            for month in range(1, 13):
                monthly_row = row.copy()
                monthly_row['date'] = pd.to_datetime(f"{row['year']}-{month:02d}-01")
                monthly_data.append(monthly_row)
        
        monthly_df = pd.DataFrame(monthly_data)
        
        # Drop the original year column
        monthly_df = monthly_df.drop('year', axis=1)
        
        print(f"  ✅ Created monthly panel: {len(monthly_df):,} observations")
        print(f"   Date range: {monthly_df['date'].min()} to {monthly_df['date'].max()}")
        print(f"  🌍 Countries: {monthly_df['iso3c'].nunique()}")
        
        return monthly_df
    
    def save_cleaned_data(self, wgi_data):
        """Save the cleaned WGI data"""
        print(f"\n Saving cleaned WGI data...")
        wgi_data.to_csv(self.output_file, index=False)
        print(f"  ✅ Saved to: {self.output_file}")
        
        # Print summary
        print(f"\n📊 CLEANED WGI DATA SUMMARY:")
        print(f"   Total observations: {len(wgi_data):,}")
        print(f"  🌍 Countries: {wgi_data['iso3c'].nunique()}")
        print(f"  📅 Date range: {wgi_data['date'].min()} to {wgi_data['date'].max()}")
        print(f"  📈 Variables: {[col for col in wgi_data.columns if col.startswith('wgi_')]}")
        
        return self.output_file

def main():
    """Main function to clean WGI data"""
    cleaner = WGICleaner()
    
    # Load WGI data
    wgi_data = cleaner.load_wgi_data()
    if wgi_data is None:
        return
    
    # Clean and filter
    filtered_data = cleaner.clean_and_filter_wgi(wgi_data)
    if len(filtered_data) == 0:
        print("❌ No data after filtering")
        return
    
    # Reshape to wide format
    wide_data = cleaner.reshape_to_wide_format(filtered_data)
    
    # Create monthly panel
    monthly_data = cleaner.create_monthly_panel(wide_data)
    
    # Save cleaned data
    cleaner.save_cleaned_data(monthly_data)
    
    print("\n✅ WGI data cleaning completed!")

if __name__ == "__main__":
    main() 