#!/usr/bin/env python3
"""
Quick Real Macro Data Integration

This script gets real macroeconomic data from reliable sources
to replace placeholder data for the thesis analysis.

Priority: GDP growth, inflation, unemployment from World Bank/OECD
"""

import pandas as pd
import numpy as np
import requests
import warnings
warnings.filterwarnings('ignore')

def get_world_bank_data():
    """Get basic macro data from World Bank API"""
    
    # Key indicators
    indicators = {
        'NY.GDP.MKTP.KD.ZG': 'gdp_growth',      # GDP growth (annual %)
        'FP.CPI.TOTL.ZG': 'inflation',          # Inflation, consumer prices (annual %)
        'SL.UEM.TOTL.ZS': 'unemployment',       # Unemployment, total (% of total labor force)
        'GC.BAL.CASH.GD.ZS': 'fiscal_balance',  # Cash surplus/deficit (% of GDP)
        'GC.DOD.TOTL.GD.ZS': 'public_debt'      # Central government debt, total (% of GDP)
    }
    
    # Major countries (subset for quick implementation)
    countries = ['USA', 'DEU', 'JPN', 'GBR', 'FRA', 'ITA', 'CAN', 'AUS', 'ESP', 'NLD', 
            'BEL', 'AUT', 'CHE', 'SWE', 'NOR', 'DNK', 'FIN', 'IRL', 'PRT', 'GRC', 
            'POL', 'CZE', 'HUN', 'SVK', 'SVN', 'EST', 'LVA', 'LTU', 'BGR', 'ROU', 
            'HRV', 'CYP', 'MLT', 'LUX', 'ISL', 'RUS', 'UKR', 'MEX', 'KOR', 'CHN', 
            'IND', 'IDN', 'MYS', 'THA', 'PHL', 'VNM', 'SGP', 'HKG', 'TWN', 'TUR', 
            'ISR', 'SAU', 'ARE', 'QAT', 'KWT', 'EGY', 'MAR', 'NGA', 'KEN', 'GHA', 
            'ETH', 'ZAF', 'BRA', 'ARG', 'CHL', 'COL', 'PER', 'URY', 'NZL']
    
    all_data = []
    
    for country in countries:
        for indicator, name in indicators.items():
            try:
                # World Bank API URL
                url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
                params = {
                    'format': 'json',
                    'date': '1990:2025',
                    'per_page': 1000
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if len(data) > 1:  # Check if data exists
                        for record in data[1]:
                            if record['value'] is not None:
                                all_data.append({
                                    'iso3c': country,
                                    'year': int(record['date']),
                                    'indicator': name,
                                    'value': float(record['value'])
                                })
                
            except Exception as e:
                print(f"Error getting {name} for {country}: {e}")
                continue
    
    if all_data:
        df = pd.DataFrame(all_data)
        # Pivot to wide format
        df_wide = df.pivot_table(index=['iso3c', 'year'], columns='indicator', values='value').reset_index()
        return df_wide
    else:
        return None

def create_simplified_controls():
    """Create simplified but realistic control variables"""
    
    # Load existing data to get structure
    merged = pd.read_csv('data/merged_panel.csv')
    countries = merged['iso3c'].unique()
    dates = pd.to_datetime(merged['date'].unique())
    
    # Create more realistic synthetic data based on actual patterns
    controls = []
    
    # Country-specific parameters (rough approximations)
    country_params = {
        'USA': {'gdp_growth': (2.5, 1.5), 'inflation': (2.5, 1.2), 'unemployment': (6.0, 2.0)},
        'DEU': {'gdp_growth': (1.8, 1.8), 'inflation': (1.8, 1.0), 'unemployment': (7.5, 2.5)},
        'JPN': {'gdp_growth': (1.0, 1.5), 'inflation': (0.5, 1.5), 'unemployment': (3.5, 1.5)},
        'GBR': {'gdp_growth': (2.2, 1.8), 'inflation': (2.8, 1.8), 'unemployment': (6.5, 2.0)},
        'FRA': {'gdp_growth': (1.5, 1.5), 'inflation': (1.8, 1.0), 'unemployment': (8.5, 2.0)},
        'ITA': {'gdp_growth': (0.8, 1.8), 'inflation': (2.0, 1.5), 'unemployment': (9.5, 3.0)},
    }
    
    for country in countries:
        # Get country parameters or use defaults
        params = country_params.get(country, {
            'gdp_growth': (2.0, 2.0), 
            'inflation': (3.0, 2.5), 
            'unemployment': (7.0, 3.0)
        })
        
        for date in dates:
            year = date.year
            
            # Add some time trends and cycles
            trend_factor = (year - 1990) / 35  # 35-year span
            cycle_factor = np.sin(2 * np.pi * (year - 1990) / 10)  # 10-year cycle
            
            controls.append({
                'iso3c': country,
                'date': date,
                'gdp_growth': np.random.normal(
                    params['gdp_growth'][0] + trend_factor * 0.5 + cycle_factor * 0.5, 
                    params['gdp_growth'][1]
                ),
                'inflation': np.random.normal(
                    params['inflation'][0] + cycle_factor * 0.8, 
                    params['inflation'][1]
                ),
                'unemployment': np.random.normal(
                    params['unemployment'][0] + trend_factor * 1.0, 
                    params['unemployment'][1]
                ),
                'current_account': np.random.normal(0, 3.0),
                'fiscal_balance': np.random.normal(-2.5, 3.0),
                'public_debt': np.random.normal(65.0, 25.0),
                # Remove credit_rating and cds_spread for now
            })
    
    return pd.DataFrame(controls)

def main():
    """Main function to get real macro data"""
    print("🔄 Getting real macroeconomic data...")
    
    # Try to get World Bank data
    wb_data = get_world_bank_data()
    
    if wb_data is not None and len(wb_data) > 0:
        print(f"✅ Got World Bank data: {len(wb_data)} records")
        
        # Expand to monthly frequency
        monthly_data = []
        for _, row in wb_data.iterrows():
            for month in range(1, 13):
                date = pd.Timestamp(year=row['year'], month=month, day=1)
                monthly_row = row.copy()
                monthly_row['date'] = date
                monthly_data.append(monthly_row)
        
        wb_monthly = pd.DataFrame(monthly_data)
        wb_monthly = wb_monthly.drop('year', axis=1)
        
        # Save real data
        wb_monthly.to_csv('data/real_macro_controls.csv', index=False)
        print("✅ Real macro data saved to data/real_macro_controls.csv")
        return wb_monthly
        
    else:
        print("❌ Could not get World Bank data, creating improved synthetic data...")

if __name__ == "__main__":
    data = main()
    print(f"\n📊 Final dataset shape: {data.shape}")
    print(f"📅 Date range: {data['date'].min()} to {data['date'].max()}")
    print(f"🌍 Countries: {data['iso3c'].nunique()}")
    print(f"📈 Variables: {list(data.columns)}")