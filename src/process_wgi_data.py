import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class WGIProcessor:
    def __init__(self):
        self.wgi_file = "data/external/Data/Control data/wgidataset_excel/wgidataset.xlsx"
        self.target_countries = [
            'ARG', 'ARM', 'AUS', 'AUT', 'BGD', 'BEL', 'BWA', 'BRA', 'BGR', 'CAN',
            'CHL', 'CHN', 'CIV', 'COL', 'HRV', 'CYP', 'CZE', 'DNK', 'EGY', 'FIN',
            'FRA', 'DEU', 'GRC', 'HKG', 'HUN', 'ISL', 'IND', 'IDN', 'IRL', 'ISR',
            'ITA', 'JPN', 'KEN', 'KOR', 'LKA', 'LVA', 'LTU', 'LUX', 'MYS', 'MLT',
            'MEX', 'NAM', 'NLD', 'NGA', 'NOR', 'NZL', 'PAK', 'PER', 'PHL', 'POL',
            'PRT', 'QAT', 'ROU', 'RUS', 'SRB', 'SGP', 'SVK', 'SVN', 'ZAF', 'ESP',
            'SWE', 'CHE', 'TWN', 'THA', 'TUR', 'UGA', 'GBR', 'USA', 'VNM', 'ZMB'
        ]
        
        # WGI indicators mapping
        self.indicators = {
            'cc': 'Control of Corruption',
            'ge': 'Government Effectiveness', 
            'rq': 'Regulatory Quality',
            'rl': 'Rule of Law',
            'va': 'Voice and Accountability',
            'pv': 'Political Stability'
        }
    
    def load_wgi_data(self):
        """Load the WGI dataset"""
        print("📊 Loading WGI dataset...")
        try:
            # Read the Excel file
            wgi_data = pd.read_excel(self.wgi_file)
            print(f"  ✅ Loaded {len(wgi_data):,} rows")
            print(f"  📋 Columns: {list(wgi_data.columns)}")
            return wgi_data
        except Exception as e:
            print(f"  ❌ Error loading WGI data: {e}")
            return None
    
    def process_wgi_data(self, wgi_data):
        """Process WGI data based on typical structure"""
        print("\n🔧 Processing WGI data...")
        
        # First, let's examine the structure
        print(f"  📊 Data shape: {wgi_data.shape}")
        print(f"  📋 Columns: {list(wgi_data.columns)}")
        
        # Look for typical WGI column patterns
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
        
        # Find indicator columns
        for code, full_name in self.indicators.items():
            for col in wgi_data.columns:
                if code.lower() in col.lower() and 'estimate' in col.lower():
                    indicator_cols[code] = col
                    break
        
        print(f"  🌍 Country column: {country_col}")
        print(f"  📅 Year column: {year_col}")
        print(f"  📈 Indicator columns: {indicator_cols}")
        
        if not country_col or not year_col:
            print("  ❌ Could not find country or year columns")
            return None
        
        # Filter for target countries
        if country_col in wgi_data.columns:
            filtered_data = wgi_data[wgi_data[country_col].isin(self.target_countries)].copy()
            print(f"  ✅ Filtered to {len(filtered_data)} rows for target countries")
        else:
            print("  ❌ Country column not found")
            return None
        
        # Select relevant columns
        selected_cols = [country_col, year_col] + list(indicator_cols.values())
        processed_data = filtered_data[selected_cols].copy()
        
        # Rename columns for consistency
        processed_data.rename(columns={
            country_col: 'iso3c',
            year_col: 'year'
        }, inplace=True)
        
        # Rename indicator columns
        for code, col in indicator_cols.items():
            processed_data.rename(columns={col: f'wgi_{code}'}, inplace=True)
        
        print(f"  ✅ Processed data shape: {processed_data.shape}")
        print(f"  📋 Final columns: {list(processed_data.columns)}")
        
        return processed_data
    
    def create_monthly_panel(self, wgi_data):
        """Convert annual WGI data to monthly panel"""
        print("\n🔄 Creating monthly panel...")
        
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
        print(f"  🌍 Countries: {monthly_df['iso3c'].nunique()}")
        
        return monthly_df
    
    def save_processed_data(self, processed_data):
        """Save the processed WGI data"""
        if processed_data is None or len(processed_data) == 0:
            print("  ❌ No data to save")
            return None
            
        output_path = "data/processed/wgi_monthly_panel.csv"
        processed_data.to_csv(output_path, index=False)
        print(f"\n💾 Processed WGI data saved to: {output_path}")
        
        # Print summary
        print(f"\n📊 WGI DATA SUMMARY:")
        print(f"  📅 Date range: {processed_data['date'].min()} to {processed_data['date'].max()}")
        print(f"  🌍 Countries: {processed_data['iso3c'].nunique()}")
        print(f"  📈 Variables: {[col for col in processed_data.columns if col.startswith('wgi_')]}")
        print(f"  📊 Total observations: {len(processed_data):,}")
        
        return output_path

def main():
    """Main function to process WGI data"""
    processor = WGIProcessor()
    
    # Load WGI data
    wgi_data = processor.load_wgi_data()
    if wgi_data is None:
        return
    
    # Process WGI data
    processed_wgi = processor.process_wgi_data(wgi_data)
    if processed_wgi is None:
        return
    
    # Create monthly panel
    monthly_wgi = processor.create_monthly_panel(processed_wgi)
    if monthly_wgi is None:
        return
    
    # Save processed data
    processor.save_processed_data(monthly_wgi)
    
    print("\n✅ WGI data processing completed!")

if __name__ == "__main__":
    main() 