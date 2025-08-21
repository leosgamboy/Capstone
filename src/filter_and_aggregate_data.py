import pandas as pd
import numpy as np
from pathlib import Path

def filter_gain_data():
    """
    Filter gain_long.csv to only include countries from data_baseline_cleaned.csv
    and append country and date information
    """
    # Read the data files
    gain_long_path = Path("data/external/Data/nd_gain_countryindex_2025/resources/gain/gain_long.csv")
    baseline_path = Path("data/processed/data_baseline_cleaned.csv")
    
    print("Reading gain_long.csv...")
    gain_long = pd.read_csv(gain_long_path)
    
    print("Reading data_baseline_cleaned.csv...")
    baseline = pd.read_csv(baseline_path)
    
    # Get unique countries from baseline data
    baseline_countries = baseline['iso3c'].unique()
    print(f"Found {len(baseline_countries)} unique countries in baseline data")
    
    # Filter gain_long to only include countries from baseline
    gain_filtered = gain_long[gain_long['iso3c'].isin(baseline_countries)].copy()
    print(f"Filtered gain_long from {len(gain_long)} to {len(gain_filtered)} rows")
    
    # Add country name mapping (you can expand this as needed)
    country_names = {
        'ARE': 'United Arab Emirates', 'ARG': 'Argentina', 'ARM': 'Armenia',
        'AUS': 'Australia', 'AUT': 'Austria', 'BEL': 'Belgium', 'BGD': 'Bangladesh',
        'BGR': 'Bulgaria', 'BRA': 'Brazil', 'BWA': 'Botswana', 'CAN': 'Canada',
        'CHE': 'Switzerland', 'CHL': 'Chile', 'CHN': 'China', 'CIV': 'Ivory Coast',
        'COL': 'Colombia', 'CYP': 'Cyprus', 'CZE': 'Czech Republic', 'DEU': 'Germany',
        'DNK': 'Denmark', 'EGY': 'Egypt', 'ESP': 'Spain', 'EST': 'Estonia',
        'FIN': 'Finland', 'FRA': 'France', 'GBR': 'United Kingdom', 'GEO': 'Georgia',
        'GRC': 'Greece', 'HRV': 'Croatia', 'HUN': 'Hungary', 'IDN': 'Indonesia',
        'IND': 'India', 'IRL': 'Ireland', 'ISL': 'Iceland', 'ISR': 'Israel',
        'ITA': 'Italy', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya',
        'KOR': 'South Korea', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'LVA': 'Latvia',
        'MAR': 'Morocco', 'MEX': 'Mexico', 'MLT': 'Malta', 'MNG': 'Mongolia',
        'MYS': 'Malaysia', 'NGA': 'Nigeria', 'NLD': 'Netherlands', 'NOR': 'Norway',
        'NZL': 'New Zealand', 'PAK': 'Pakistan', 'PER': 'Peru', 'PHL': 'Philippines',
        'POL': 'Poland', 'PRT': 'Portugal', 'ROU': 'Romania', 'RUS': 'Russia',
        'SAU': 'Saudi Arabia', 'SGP': 'Singapore', 'SVK': 'Slovakia', 'SVN': 'Slovenia',
        'SWE': 'Sweden', 'THA': 'Thailand', 'TUN': 'Tunisia', 'TUR': 'Turkey',
        'UKR': 'Ukraine', 'URY': 'Uruguay', 'USA': 'United States', 'VNM': 'Vietnam',
        'ZAF': 'South Africa', 'ZWE': 'Zimbabwe'
    }
    
    # Add country name column
    gain_filtered['country'] = gain_filtered['iso3c'].map(country_names)
    
    # Convert date to datetime and extract year
    gain_filtered['date'] = pd.to_datetime(gain_filtered['date'], format='%Y')
    gain_filtered['year'] = gain_filtered['date'].dt.year
    
    # Save filtered gain data
    output_path = Path("data/processed/gain_filtered.csv")
    gain_filtered.to_csv(output_path, index=False)
    print(f"Saved filtered gain data to {output_path}")
    
    return gain_filtered, baseline

def create_yearly_baseline_data(baseline):
    """
    Create yearly aggregated data from monthly baseline data
    """
    print("Creating yearly aggregated baseline data...")
    
    # Convert date to datetime
    baseline['date'] = pd.to_datetime(baseline['date'])
    baseline['year'] = baseline['date'].dt.year
    
    # Define numeric columns for aggregation (exclude date, iso3c, year)
    numeric_cols = baseline.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [col for col in numeric_cols if col != 'year']
    
    print(f"Aggregating {len(numeric_cols)} numeric variables by year and country")
    
    # Group by year and country, calculate mean for numeric variables
    yearly_data = baseline.groupby(['year', 'iso3c'])[numeric_cols].mean().reset_index()
    
    # Add country names
    country_names = {
        'ARE': 'United Arab Emirates', 'ARG': 'Argentina', 'ARM': 'Armenia',
        'AUS': 'Australia', 'AUT': 'Austria', 'BEL': 'Belgium', 'BGD': 'Bangladesh',
        'BGR': 'Bulgaria', 'BRA': 'Brazil', 'BWA': 'Botswana', 'CAN': 'Canada',
        'CHE': 'Switzerland', 'CHL': 'Chile', 'CHN': 'China', 'CIV': 'Ivory Coast',
        'COL': 'Colombia', 'CYP': 'Cyprus', 'CZE': 'Czech Republic', 'DEU': 'Germany',
        'DNK': 'Denmark', 'EGY': 'Egypt', 'ESP': 'Spain', 'EST': 'Estonia',
        'FIN': 'Finland', 'FRA': 'France', 'GBR': 'United Kingdom', 'GEO': 'Georgia',
        'GRC': 'Greece', 'HRV': 'Croatia', 'HUN': 'Hungary', 'IDN': 'Indonesia',
        'IND': 'India', 'IRL': 'Ireland', 'ISL': 'Iceland', 'ISR': 'Israel',
        'ITA': 'Italy', 'JPN': 'Japan', 'KAZ': 'Kazakhstan', 'KEN': 'Kenya',
        'KOR': 'South Korea', 'LTU': 'Lithuania', 'LUX': 'Luxembourg', 'LVA': 'Latvia',
        'MAR': 'Morocco', 'MEX': 'Mexico', 'MLT': 'Malta', 'MNG': 'Mongolia',
        'MYS': 'Malaysia', 'NGA': 'Nigeria', 'NLD': 'Netherlands', 'NOR': 'Norway',
        'NZL': 'New Zealand', 'PAK': 'Pakistan', 'PER': 'Peru', 'PHL': 'Philippines',
        'POL': 'Poland', 'PRT': 'Portugal', 'ROU': 'Romania', 'RUS': 'Russia',
        'SAU': 'Saudi Arabia', 'SGP': 'Singapore', 'SVK': 'Slovakia', 'SVN': 'Slovenia',
        'SWE': 'Sweden', 'THA': 'Thailand', 'TUN': 'Tunisia', 'TUR': 'Turkey',
        'UKR': 'Ukraine', 'URY': 'Uruguay', 'USA': 'United States', 'VNM': 'Vietnam',
        'ZAF': 'South Africa', 'ZWE': 'Zimbabwe'
    }
    
    yearly_data['country'] = yearly_data['iso3c'].map(country_names)
    
    # Reorder columns to put country name after iso3c
    cols = ['year', 'iso3c', 'country'] + [col for col in yearly_data.columns if col not in ['year', 'iso3c', 'country']]
    yearly_data = yearly_data[cols]
    
    # Save yearly aggregated data
    output_path = Path("data/processed/baseline_yearly_aggregated.csv")
    yearly_data.to_csv(output_path, index=False)
    print(f"Saved yearly aggregated baseline data to {output_path}")
    
    return yearly_data

def main():
    """
    Main function to execute the data filtering and aggregation
    """
    print("Starting data filtering and aggregation process...")
    
    # Filter gain data
    gain_filtered, baseline = filter_gain_data()
    
    # Create yearly baseline data
    yearly_baseline = create_yearly_baseline_data(baseline)
    
    # Print summary statistics
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    print(f"Filtered gain data: {len(gain_filtered)} rows")
    print(f"Yearly baseline data: {len(yearly_baseline)} rows")
    print(f"Countries in filtered data: {gain_filtered['iso3c'].nunique()}")
    print(f"Years covered: {gain_filtered['year'].min()} - {gain_filtered['year'].max()}")
    print(f"Variables in yearly data: {len(yearly_baseline.columns) - 3}")  # -3 for year, iso3c, country
    
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()
