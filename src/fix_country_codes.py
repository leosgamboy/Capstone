import pandas as pd

def fix_country_codes():
    """
    Fix country names in the merged dataset by converting to proper 3-letter ISO codes
    """
    print("Loading merged dataset...")
    merged_data = pd.read_csv("data/processed/merged_all_variables.csv")
    
    print(f"Original dataset shape: {merged_data.shape}")
    print(f"Unique countries before fixing: {len(merged_data['iso3c'].unique())}")
    
    # Define the country name mappings
    country_mappings = {
        'ESTONIA': 'EST',
        'ETHIOPIA': 'ETH', 
        'IVORY COAST': 'CIV',
        'GHANA': 'GHA',
        'KUWAIT': 'KWT',
        'MOROCCO': 'MAR',
        'SAUDI ARABIA': 'SAU',
        'UKRAINE': 'UKR',
        'UNITED ARAB EMIRATES': 'ARE',
        'URUGUAY': 'URY'
    }
    
    # Show current unique countries
    print("\nCurrent unique countries:")
    unique_countries = sorted(merged_data['iso3c'].unique())
    for country in unique_countries:
        print(f"  {country}")
    
    # Apply the mappings
    print(f"\nApplying country code mappings...")
    for old_name, new_code in country_mappings.items():
        if old_name in merged_data['iso3c'].values:
            count = len(merged_data[merged_data['iso3c'] == old_name])
            merged_data['iso3c'] = merged_data['iso3c'].replace(old_name, new_code)
            print(f"  {old_name} -> {new_code} ({count} observations)")
        else:
            print(f"  {old_name} not found in dataset")
    
    # Show updated unique countries
    print(f"\nUpdated unique countries:")
    unique_countries_after = sorted(merged_data['iso3c'].unique())
    for country in unique_countries_after:
        print(f"  {country}")
    
    print(f"\nUnique countries after fixing: {len(unique_countries_after)}")
    
    # Save the updated dataset
    output_path = "data/processed/merged_all_variables_fixed.csv"
    merged_data.to_csv(output_path, index=False)
    print(f"\nUpdated dataset saved to: {output_path}")
    
    # Also update the missing data tables
    print("\nUpdating missing data tables...")
    
    # Update missing_data_by_country.csv
    try:
        missing_by_country = pd.read_csv("data/processed/missing_data_by_country.csv")
        print(f"Updating missing_data_by_country.csv...")
        
        for old_name, new_code in country_mappings.items():
            if old_name in missing_by_country['Country'].values:
                count = len(missing_by_country[missing_by_country['Country'] == old_name])
                missing_by_country['Country'] = missing_by_country['Country'].replace(old_name, new_code)
                print(f"  {old_name} -> {new_code} ({count} rows)")
        
        missing_by_country.to_csv("data/processed/missing_data_by_country_fixed.csv", index=False)
        print(f"Updated missing_data_by_country.csv saved")
    except FileNotFoundError:
        print("missing_data_by_country.csv not found")
    
    # Update missing_data_table_clean.csv
    try:
        missing_clean = pd.read_csv("data/processed/missing_data_table_clean.csv")
        print(f"Updating missing_data_table_clean.csv...")
        
        for old_name, new_code in country_mappings.items():
            if old_name in missing_clean['Country'].values:
                count = len(missing_clean[missing_clean['Country'] == old_name])
                missing_clean['Country'] = missing_clean['Country'].replace(old_name, new_code)
                print(f"  {old_name} -> {new_code} ({count} rows)")
        
        missing_clean.to_csv("data/processed/missing_data_table_clean_fixed.csv", index=False)
        print(f"Updated missing_data_table_clean.csv saved")
    except FileNotFoundError:
        print("missing_data_table_clean.csv not found")
    
    # Update missing_data_table_enhanced.csv
    try:
        missing_enhanced = pd.read_csv("data/processed/missing_data_table_enhanced.csv")
        print(f"Updating missing_data_table_enhanced.csv...")
        
        for old_name, new_code in country_mappings.items():
            if old_name in missing_enhanced['Country'].values:
                count = len(missing_enhanced[missing_enhanced['Country'] == old_name])
                missing_enhanced['Country'] = missing_enhanced['Country'].replace(old_name, new_code)
                print(f"  {old_name} -> {new_code} ({count} rows)")
        
        missing_enhanced.to_csv("data/processed/missing_data_table_enhanced_fixed.csv", index=False)
        print(f"Updated missing_data_table_enhanced.csv saved")
    except FileNotFoundError:
        print("missing_data_table_enhanced.csv not found")
    
    # Update missing_data_heatmap_top20.csv
    try:
        missing_heatmap = pd.read_csv("data/processed/missing_data_heatmap_top20.csv")
        print(f"Updating missing_data_heatmap_top20.csv...")
        
        for old_name, new_code in country_mappings.items():
            if old_name in missing_heatmap['Country'].values:
                count = len(missing_heatmap[missing_heatmap['Country'] == old_name])
                missing_heatmap['Country'] = missing_heatmap['Country'].replace(old_name, new_code)
                print(f"  {old_name} -> {new_code} ({count} rows)")
        
        missing_heatmap.to_csv("data/processed/missing_data_heatmap_top20_fixed.csv", index=False)
        print(f"Updated missing_data_heatmap_top20.csv saved")
    except FileNotFoundError:
        print("missing_data_heatmap_top20.csv not found")
    
    print("\nAll files updated successfully!")
    
    # Show a sample of the updated data
    print("\n" + "="*80)
    print("SAMPLE OF UPDATED DATASET")
    print("="*80)
    print(merged_data[['date', 'iso3c', 'sovereign_yield']].head(10))
    
    return merged_data

if __name__ == "__main__":
    fix_country_codes()




