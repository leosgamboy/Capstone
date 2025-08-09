import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

class WGIIntegrator:
    def __init__(self):
        self.bond_yields_file = "data/merged_panel.csv"
        self.wgi_file = "data/processed/wgi_monthly_panel.csv"
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
    
    def load_bond_yields(self):
        """Load bond yields data"""
        print("📊 Loading bond yields data...")
        try:
            bond_data = pd.read_csv(self.bond_yields_file)
            bond_data['date'] = pd.to_datetime(bond_data['date'])
            print(f"  ✅ Loaded {len(bond_data):,} bond yield observations")
            print(f"  🌍 Countries: {bond_data['iso3c'].nunique()}")
            print(f"  📅 Date range: {bond_data['date'].min()} to {bond_data['date'].max()}")
            return bond_data
        except Exception as e:
            print(f"  ❌ Error loading bond yields: {e}")
            return None
    
    def load_wgi_data(self):
        """Load WGI data"""
        print("\n📊 Loading WGI data...")
        try:
            wgi_data = pd.read_csv(self.wgi_file)
            wgi_data['date'] = pd.to_datetime(wgi_data['date'])
            print(f"  ✅ Loaded {len(wgi_data):,} WGI observations")
            print(f"  🌍 Countries: {wgi_data['iso3c'].nunique()}")
            print(f"  📅 Date range: {wgi_data['date'].min()} to {wgi_data['date'].max()}")
            print(f"  📈 WGI variables: {[col for col in wgi_data.columns if col.startswith('wgi_')]}")
            return wgi_data
        except Exception as e:
            print(f"  ❌ Error loading WGI data: {e}")
            return None
    
    def load_macro_data(self):
        """Load macro controls data"""
        print("\n📊 Loading macro controls data...")
        try:
            macro_data = pd.read_csv(self.macro_file)
            macro_data['date'] = pd.to_datetime(macro_data['date'])
            print(f"  ✅ Loaded {len(macro_data):,} macro observations")
            print(f"  🌍 Countries: {macro_data['iso3c'].nunique()}")
            print(f"  📅 Date range: {macro_data['date'].min()} to {macro_data['date'].max()}")
            return macro_data
        except Exception as e:
            print(f"  ❌ Error loading macro data: {e}")
            return None
    
    def merge_datasets(self, bond_data, wgi_data, macro_data):
        """Merge all datasets"""
        print("\n🔄 Merging datasets...")
        
        # Start with bond yields as base
        merged = bond_data.copy()
        print(f"  📊 Starting with {len(merged):,} bond yield observations")
        
        # Merge WGI data
        if wgi_data is not None and len(wgi_data) > 0:
            print(f"  🔗 Merging WGI data...")
            merged = merged.merge(wgi_data, on=['iso3c', 'date'], how='left')
            print(f"    ✅ After WGI merge: {len(merged):,} observations")
            print(f"    📈 WGI coverage: {merged['wgi_cc'].notna().sum():,} observations")
        else:
            print(f"  ⚠️  No WGI data to merge")
        
        # Merge macro data
        if macro_data is not None and len(macro_data) > 0:
            print(f"  🔗 Merging macro controls...")
            merged = merged.merge(macro_data, on=['iso3c', 'date'], how='left')
            print(f"    ✅ After macro merge: {len(merged):,} observations")
            print(f"    📈 Macro coverage: {merged['gdp_growth'].notna().sum():,} observations")
        else:
            print(f"  ⚠️  No macro data to merge")
        
        return merged
    
    def filter_for_analysis(self, merged_data):
        """Filter data for analysis-ready dataset"""
        print("\n🎯 Filtering for analysis...")
        
        # Filter for target countries
        initial_count = len(merged_data)
        merged_data = merged_data[merged_data['iso3c'].isin(self.target_countries)].copy()
        print(f"  🌍 Filtered to target countries: {len(merged_data):,} observations")
        
        # Filter for reasonable date range (1995-2023)
        merged_data = merged_data[
            (merged_data['date'] >= '1995-01-01') & 
            (merged_data['date'] <= '2023-12-31')
        ].copy()
        print(f"  📅 Filtered to 1995-2023: {len(merged_data):,} observations")
        
        # Check data quality
        print(f"\n📊 DATA QUALITY CHECK:")
        print(f"  📈 Bond yields: {merged_data['bond_yield'].notna().sum():,} observations")
        print(f"  🌱 ND-GAIN: {merged_data['nd_gain'].notna().sum():,} observations")
        
        # Check WGI coverage
        wgi_vars = [col for col in merged_data.columns if col.startswith('wgi_')]
        for var in wgi_vars:
            coverage = merged_data[var].notna().sum()
            print(f"  🏛️  {var}: {coverage:,} observations")
        
        # Check macro coverage
        macro_vars = ['gdp_growth', 'inflation', 'public_debt', 'unemployment']
        for var in macro_vars:
            if var in merged_data.columns:
                coverage = merged_data[var].notna().sum()
                print(f"  📊 {var}: {coverage:,} observations")
        
        return merged_data
    
    def save_integrated_data(self, merged_data):
        """Save the integrated dataset"""
        print(f"\n💾 Saving integrated dataset...")
        merged_data.to_csv(self.output_file, index=False)
        print(f"  ✅ Saved to: {self.output_file}")
        
        # Create summary
        print(f"\n📊 FINAL DATASET SUMMARY:")
        print(f"  📊 Total observations: {len(merged_data):,}")
        print(f"  🌍 Countries: {merged_data['iso3c'].nunique()}")
        print(f"  📅 Date range: {merged_data['date'].min()} to {merged_data['date'].max()}")
        print(f"  📈 Variables: {list(merged_data.columns)}")
        
        # Check for countries with good coverage
        good_coverage = merged_data.groupby('iso3c').agg({
            'bond_yield': 'count',
            'nd_gain': 'count',
            'wgi_cc': 'count'
        }).reset_index()
        
        print(f"\n🌍 COUNTRIES WITH GOOD COVERAGE:")
        for _, row in good_coverage.head(10).iterrows():
            print(f"  {row['iso3c']}: {row['bond_yield']} bond obs, {row['nd_gain']} ND-GAIN obs, {row['wgi_cc']} WGI obs")
        
        return self.output_file

def main():
    """Main function to integrate WGI data"""
    integrator = WGIIntegrator()
    
    # Load all datasets
    bond_data = integrator.load_bond_yields()
    wgi_data = integrator.load_wgi_data()
    macro_data = integrator.load_macro_data()
    
    if bond_data is None:
        print("❌ Cannot proceed without bond yield data")
        return
    
    # Merge datasets
    merged_data = integrator.merge_datasets(bond_data, wgi_data, macro_data)
    
    # Filter for analysis
    analysis_data = integrator.filter_for_analysis(merged_data)
    
    # Save integrated data
    integrator.save_integrated_data(analysis_data)
    
    print("\n✅ WGI integration completed!")

if __name__ == "__main__":
    main() 