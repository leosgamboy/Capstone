import pandas as pd
import numpy as np

def examine_wgi_structure():
    """Examine the WGI dataset structure"""
    wgi_file = "data/external/Data/Control data/wgidataset_excel/wgidataset.xlsx"
    
    print("🔍 Examining WGI dataset structure...")
    
    try:
        # Read the Excel file
        wgi_data = pd.read_excel(wgi_file)
        print(f"✅ Successfully loaded WGI data")
        print(f"📊 Shape: {wgi_data.shape}")
        print(f"📋 Columns: {list(wgi_data.columns)}")
        
        # Show first few rows
        print(f"\n📄 First 5 rows:")
        print(wgi_data.head())
        
        # Check for country codes
        country_cols = [col for col in wgi_data.columns if 'code' in col.lower() or 'country' in col.lower()]
        print(f"\n🌍 Country columns: {country_cols}")
        
        # Check for year columns
        year_cols = [col for col in wgi_data.columns if 'year' in col.lower()]
        print(f"📅 Year columns: {year_cols}")
        
        # Check for indicator columns
        indicators = ['cc', 'ge', 'rq', 'rl', 'va', 'pv']
        for indicator in indicators:
            matching_cols = [col for col in wgi_data.columns if indicator.lower() in col.lower()]
            print(f"📈 {indicator}: {matching_cols}")
        
        # Check for estimate columns
        estimate_cols = [col for col in wgi_data.columns if 'estimate' in col.lower()]
        print(f"📊 Estimate columns: {estimate_cols}")
        
        return wgi_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    examine_wgi_structure() 