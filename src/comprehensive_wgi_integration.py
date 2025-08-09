import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class ComprehensiveWGIIntegrator:
    def __init__(self):
        self.wgi_file = "data/external/Data/Control data/wgidataset_excel/wgidataset.xlsx"
        self.bond_yields_file = "data/merged_panel.csv"
        self.macro_file = "data/real_macro_controls.csv"
        self.output_file = "data/merged_panel_with_wgi.csv"
        
        # Target countries for analysis
        self.target_countries = [
            'USA', 'DEU', 'JPN', 'GBR', 'FRA', 'ITA', 'CAN', 'AUS', 'ESP', 'NLD', 
            'BEL', 'AUT', 'CHE', 'SWE', 'NOR', 'DNK', 'FIN', 'IRL', 'PRT', 'GRC', 
            'POL', 'CZE', 'HUN', 'SVK', 'SVN', 'EST', 'LVA', 'LTU', 'BGR', 'ROU', 
            'HRV', 'CYP', 'MLT', 'LUX', 'ISL', 'RUS', 'UKR', 'MEX', 'KOR', 'CHN', 
            'IND', 'IDN', 'MYS', 'THA', 'PHL', 'VNM', 'SGP', 'HKG', 'TWN', 'TUR', 
            'ISR', 'SAU', 'ARE', 'QAT', 'KWT', 'EGY', 'MAR', 'NGA', 'KEN', 'GHA', 
            'ETH', 'ZAF', 'BRA', 'ARG', 'CHL', 'COL', 'PER', 'URY', 'NZL'
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
    
    def load_and_process_wgi(self):
        """Load and process WGI data"""
        print("📊 Loading and processing WGI data...")
        
        try:
            # Load WGI Excel file
            wgi_data = pd.read_excel(self.wgi_file)
            print(f"  ✅ Loaded {len(wgi_data):,} rows from WGI file")
            print(f"  📋 Columns: {list(wgi_data.columns)}")
            
            # Examine structure and find relevant columns
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
            filtered_data = wgi_data[wgi_data[country_col].isin(self.target_countries)].copy()
            print(f"  ✅ Filtered to {len(filtered_data)} rows for target countries")
            
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
            
            print(f"  ✅ Processed WGI data shape: {processed_data.shape}")
            print(f"  📋 Final columns: {list(processed_data.columns)}")
            
            return processed_data
            
        except Exception as e:
            print(f"  ❌ Error processing WGI data: {e}")
            return None
    
    def create_monthly_wgi_panel(self, wgi_data):
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
        print(f"  🌍 Countries: {monthly_df['iso3c'].nunique()}")
        
        return monthly_df
    
    def load_existing_data(self):
        """Load existing bond yields and macro data"""
        print("\n📊 Loading existing data...")
        
        # Load bond yields
        try:
            bond_data = pd.read_csv(self.bond_yields_file)
            bond_data['date'] = pd.to_datetime(bond_data['date'])
            print(f"  ✅ Bond yields: {len(bond_data):,} observations")
        except Exception as e:
            print(f"  ❌ Error loading bond yields: {e}")
            bond_data = None
        
        # Load macro controls
        try:
            macro_data = pd.read_csv(self.macro_file)
            macro_data['date'] = pd.to_datetime(macro_data['date'])
            print(f"  ✅ Macro controls: {len(macro_data):,} observations")
        except Exception as e:
            print(f"  ❌ Error loading macro data: {e}")
            macro_data = None
        
        return bond_data, macro_data
    
    def integrate_all_data(self, bond_data, wgi_monthly, macro_data):
        """Integrate all datasets"""
        print("\n🔄 Integrating all datasets...")
        
        if bond_data is None:
            print("  ❌ Cannot proceed without bond yield data")
            return None
        
        # Start with bond yields as base
        merged = bond_data.copy()
        print(f"  📊 Starting with {len(merged):,} bond yield observations")
        
        # Merge WGI data
        if wgi_monthly is not None and len(wgi_monthly) > 0:
            print(f"  🔗 Merging WGI data...")
            merged = merged.merge(wgi_monthly, on=['iso3c', 'date'], how='left')
            print(f"    ✅ After WGI merge: {len(merged):,} observations")
            
            # Check WGI coverage
            wgi_vars = [col for col in merged.columns if col.startswith('wgi_')]
            for var in wgi_vars:
                coverage = merged[var].notna().sum()
                print(f"    📈 {var}: {coverage:,} observations")
        else:
            print(f"  ⚠️  No WGI data to merge")
        
        # Merge macro data
        if macro_data is not None and len(macro_data) > 0:
            print(f"  🔗 Merging macro controls...")
            merged = merged.merge(macro_data, on=['iso3c', 'date'], how='left')
            print(f"    ✅ After macro merge: {len(merged):,} observations")
            
            # Check macro coverage
            macro_vars = ['gdp_growth', 'inflation', 'public_debt', 'unemployment']
            for var in macro_vars:
                if var in merged.columns:
                    coverage = merged[var].notna().sum()
                    print(f"    📊 {var}: {coverage:,} observations")
        else:
            print(f"  ⚠️  No macro data to merge")
        
        return merged
    
    def filter_and_save(self, merged_data):
        """Filter data and save final dataset"""
        print("\n🎯 Filtering and saving final dataset...")
        
        # Filter for target countries
        merged_data = merged_data[merged_data['iso3c'].isin(self.target_countries)].copy()
        print(f"  🌍 Filtered to target countries: {len(merged_data):,} observations")
        
        # Filter for reasonable date range (1995-2023)
        merged_data = merged_data[
            (merged_data['date'] >= '1995-01-01') & 
            (merged_data['date'] <= '2023-12-31')
        ].copy()
        print(f"  📅 Filtered to 1995-2023: {len(merged_data):,} observations")
        
        # Save final dataset
        merged_data.to_csv(self.output_file, index=False)
        print(f"  💾 Saved to: {self.output_file}")
        
        # Create comprehensive summary
        print(f"\n📊 FINAL DATASET SUMMARY:")
        print(f"  📊 Total observations: {len(merged_data):,}")
        print(f"  🌍 Countries: {merged_data['iso3c'].nunique()}")
        print(f"  📅 Date range: {merged_data['date'].min()} to {merged_data['date'].max()}")
        
        # Data quality summary
        print(f"\n📈 DATA QUALITY SUMMARY:")
        print(f"  📈 Bond yields: {merged_data['bond_yield'].notna().sum():,} observations")
        print(f"  🌱 ND-GAIN: {merged_data['nd_gain'].notna().sum():,} observations")
        
        # WGI coverage
        wgi_vars = [col for col in merged_data.columns if col.startswith('wgi_')]
        for var in wgi_vars:
            coverage = merged_data[var].notna().sum()
            print(f"  🏛️  {var}: {coverage:,} observations")
        
        # Macro coverage
        macro_vars = ['gdp_growth', 'inflation', 'public_debt', 'unemployment']
        for var in macro_vars:
            if var in merged_data.columns:
                coverage = merged_data[var].notna().sum()
                print(f"  📊 {var}: {coverage:,} observations")
        
        # Countries with good coverage
        print(f"\n🌍 TOP COUNTRIES BY COVERAGE:")
        coverage_summary = merged_data.groupby('iso3c').agg({
            'bond_yield': 'count',
            'nd_gain': 'count',
            'wgi_cc': 'count',
            'gdp_growth': 'count'
        }).reset_index()
        
        coverage_summary = coverage_summary.sort_values('bond_yield', ascending=False)
        for _, row in coverage_summary.head(10).iterrows():
            print(f"  {row['iso3c']}: {row['bond_yield']} bond, {row['nd_gain']} ND-GAIN, {row['wgi_cc']} WGI, {row['gdp_growth']} macro")
        
        return self.output_file

def main():
    """Main function to process and integrate WGI data"""
    integrator = ComprehensiveWGIIntegrator()
    
    # Load and process WGI data
    wgi_annual = integrator.load_and_process_wgi()
    if wgi_annual is None:
        print("❌ Failed to process WGI data")
        return
    
    # Create monthly WGI panel
    wgi_monthly = integrator.create_monthly_wgi_panel(wgi_annual)
    if wgi_monthly is None:
        print("❌ Failed to create monthly WGI panel")
        return
    
    # Load existing data
    bond_data, macro_data = integrator.load_existing_data()
    
    # Integrate all data
    merged_data = integrator.integrate_all_data(bond_data, wgi_monthly, macro_data)
    if merged_data is None:
        print("❌ Failed to integrate data")
        return
    
    # Filter and save final dataset
    integrator.filter_and_save(merged_data)
    
    print("\n✅ Comprehensive WGI integration completed!")

if __name__ == "__main__":
    main() 