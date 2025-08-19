#!/usr/bin/env python3
"""
Comprehensive WGI Data Cleaner
Processes World Governance Indicators data for countries in yield spreads dataset
"""

import pandas as pd
import numpy as np
import warnings
from pathlib import Path
import os
warnings.filterwarnings('ignore')

# Import the updated country mapping
from country_iso_mapping import COUNTRY_ISO_MAPPING

class ComprehensiveWGICleaner:
    def __init__(self):
        self.wgi_file = "data/external/Data/Control data/wgidataset_excel/wgidataset.xlsx"
        self.output_file = "data/processed/wgi_comprehensive_cleaned.csv"
        
        # Get target countries from the updated mapping (71 from yields + USA)
        self.target_countries = list(COUNTRY_ISO_MAPPING.values())
        print(f"🎯 Target countries: {len(self.target_countries)}")
        
        # WGI indicators mapping
        self.indicators = {
            'cc': 'Control of Corruption',
            'ge': 'Government Effectiveness', 
            'rq': 'Regulatory Quality',
            'rl': 'Rule of Law',
            'va': 'Voice and Accountability',
            'pv': 'Political Stability'
        }
    
    def load_and_examine_wgi(self):
        """Load and examine WGI data structure"""
        print("📊 Loading and examining WGI data...")
        
        try:
            # Load WGI Excel file
            wgi_data = pd.read_excel(self.wgi_file)
            print(f"  ✅ Loaded {len(wgi_data):,} rows from WGI file")
            print(f"  📋 Total columns: {len(wgi_data.columns)}")
            
            # Show first few rows to understand structure
            print(f"\n  📋 First few columns: {list(wgi_data.columns[:10])}")
            print(f"  📋 Sample data shape: {wgi_data.shape}")
            
            return wgi_data
            
        except Exception as e:
            print(f"  ❌ Error loading WGI data: {e}")
            return None
    
    def identify_wgi_structure(self, wgi_data):
        """Identify the structure of WGI data"""
        print("\n🔍 Identifying WGI data structure...")
        
        # Look for key columns
        country_col = None
        year_col = None
        indicator_cols = {}
        
        # Find country code column
        for col in wgi_data.columns:
            if 'code' in col.lower() or 'country' in col.lower():
                country_col = col
                break
        
        # Find year column
        for col in wgi_data.columns:
            if 'year' in col.lower():
                year_col = col
                break
        
        # Find indicator columns for each WGI component
        for code, full_name in self.indicators.items():
            for col in wgi_data.columns:
                if code.lower() in col.lower() and 'estimate' in col.lower():
                    indicator_cols[code] = col
                    break
        
        print(f"  🌍 Country column: {country_col}")
        print(f"  📅 Year column: {year_col}")
        print(f"  📈 Indicator columns found: {len(indicator_cols)}")
        
        for code, col in indicator_cols.items():
            print(f"    {code}: {col}")
        
        if not country_col or not year_col:
            print("  ❌ Could not find country or year columns")
            return None, None, None
        
        return country_col, year_col, indicator_cols
    
    def process_wgi_data(self, wgi_data, country_col, year_col, indicator_cols):
        """Process WGI data for target countries"""
        print("\n🔄 Processing WGI data...")
        
        # Filter for target countries
        filtered_data = wgi_data[wgi_data[country_col].isin(self.target_countries)].copy()
        print(f"  ✅ Filtered to {len(filtered_data)} rows for target countries")
        
        # Check which countries are missing
        found_countries = set(filtered_data[country_col].unique())
        missing_countries = set(self.target_countries) - found_countries
        
        if missing_countries:
            print(f"  ⚠️  Missing countries ({len(missing_countries)}): {sorted(missing_countries)}")
        else:
            print(f"  ✅ All target countries found!")
        
        # Select relevant columns
        selected_cols = [country_col, year_col] + list(indicator_cols.values())
        processed_data = filtered_data[selected_cols].copy()
        
        # Rename columns for consistency
        processed_data.rename(columns={
            country_col: 'iso3',
            year_col: 'year'
        }, inplace=True)
        
        # Rename indicator columns
        for code, col in indicator_cols.items():
            processed_data.rename(columns={col: f'wgi_{code}'}, inplace=True)
        
        print(f"  ✅ Processed WGI data shape: {processed_data.shape}")
        print(f"  📋 Final columns: {list(processed_data.columns)}")
        
        return processed_data, missing_countries
    
    def create_monthly_panel(self, wgi_data):
        """Convert annual WGI data to monthly panel"""
        print("\n🔄 Creating monthly WGI panel...")
        
        if wgi_data is None or len(wgi_data) == 0:
            print("  ❌ No WGI data to process")
            return None
        
        # Convert year to datetime (first day of year)
        wgi_data['date'] = pd.to_datetime(wgi_data['year'].astype(str) + '-01-01')
        
        # Create monthly frequency for each country-year
        monthly_data = []
        
        for _, row in wgi_data.iterrows():
            # Create 12 monthly observations for each year
            for month in range(1, 13):
                monthly_row = row.copy()
                monthly_row['date'] = pd.to_datetime(f"{row['year']}-{month:02d}-01")
                monthly_data.append(monthly_row)
        
        monthly_df = pd.DataFrame(monthly_data)
        
        # Drop the original year column
        if 'year' in monthly_df.columns:
            monthly_df = monthly_df.drop('year', axis=1)
        
        print(f"  ✅ Created monthly panel: {len(monthly_df):,} observations")
        print(f"  📅 Date range: {monthly_df['date'].min()} to {monthly_df['date'].max()}")
        print(f"  🌍 Countries: {monthly_df['iso3'].nunique()}")
        
        return monthly_df
    
    def save_and_summarize(self, monthly_data, missing_countries):
        """Save the cleaned data and provide summary"""
        print("\n💾 Saving and summarizing...")
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Save to CSV
        monthly_data.to_csv(self.output_file, index=False)
        print(f"  ✅ Saved to: {self.output_file}")
        
        # Comprehensive summary
        print(f"\n📊 COMPREHENSIVE WGI DATASET SUMMARY:")
        print(f"  📊 Total observations: {len(monthly_data):,}")
        print(f"  🌍 Countries: {monthly_data['iso3'].nunique()}")
        print(f"  📅 Date range: {monthly_data['date'].min()} to {monthly_data['date'].max()}")
        
        # Data quality summary
        print(f"\n📈 DATA QUALITY SUMMARY:")
        wgi_vars = [col for col in monthly_data.columns if col.startswith('wgi_')]
        for var in wgi_vars:
            coverage = monthly_data[var].notna().sum()
            print(f"  🏛️  {var}: {coverage:,} observations")
        
        # Country coverage summary
        print(f"\n🌍 COUNTRY COVERAGE SUMMARY:")
        coverage_summary = monthly_data.groupby('iso3').agg({
            'wgi_cc': 'count',
            'wgi_ge': 'count',
            'wgi_rq': 'count',
            'wgi_rl': 'count',
            'wgi_va': 'count',
            'wgi_pv': 'count'
        }).reset_index()
        
        # Calculate average coverage across all indicators
        wgi_cols = [col for col in coverage_summary.columns if col.startswith('wgi_')]
        coverage_summary['avg_coverage'] = coverage_summary[wgi_cols].mean(axis=1)
        
        # Sort by average coverage
        coverage_summary = coverage_summary.sort_values('avg_coverage', ascending=False)
        
        print(f"  Top 10 countries by coverage:")
        for _, row in coverage_summary.head(10).iterrows():
            print(f"    {row['iso3']}: {row['avg_coverage']:.0f} months avg")
        
        print(f"\n  Bottom 10 countries by coverage:")
        for _, row in coverage_summary.tail(10).iterrows():
            print(f"    {row['iso3']}: {row['avg_coverage']:.0f} months avg")
        
        # Missing countries report
        if missing_countries:
            print(f"\n⚠️  MISSING COUNTRIES REPORT:")
            print(f"  Total missing: {len(missing_countries)}")
            print(f"  Missing countries: {sorted(missing_countries)}")
            print(f"  These countries are in your target list but not found in WGI data")
        
        return self.output_file

def main():
    """Main function to process and clean WGI data"""
    print("🚀 Starting Comprehensive WGI Data Cleaner")
    print("=" * 50)
    
    cleaner = ComprehensiveWGICleaner()
    
    # Load and examine WGI data
    wgi_data = cleaner.load_and_examine_wgi()
    if wgi_data is None:
        print("❌ Failed to load WGI data")
        return
    
    # Identify WGI structure
    country_col, year_col, indicator_cols = cleaner.identify_wgi_structure(wgi_data)
    if country_col is None:
        print("❌ Failed to identify WGI structure")
        return
    
    # Process WGI data
    processed_data, missing_countries = cleaner.process_wgi_data(wgi_data, country_col, year_col, indicator_cols)
    if processed_data is None:
        print("❌ Failed to process WGI data")
        return
    
    # Create monthly panel
    monthly_data = cleaner.create_monthly_panel(processed_data)
    if monthly_data is None:
        print("❌ Failed to create monthly panel")
        return
    
    # Save and summarize
    cleaner.save_and_summarize(monthly_data, missing_countries)
    
    print("\n✅ Comprehensive WGI cleaning completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
