#!/usr/bin/env python3
"""
Comprehensive Real Data Integration

This script integrates ALL available real control data:
- IMF CPI data (inflation)
- IMF WEO data (unemployment, debt, expenditure)
- World Governance Indicators (6 governance measures)
- ND-GAIN vulnerability data
- Real bond yield data

Creates a high-quality dataset for Double ML analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class ComprehensiveDataIntegrator:
    def __init__(self):
        self.data_dir = Path('data')
        self.external_dir = self.data_dir / 'external' / 'Data'
        self.processed_dir = self.data_dir / 'processed'
        
        # Country code mapping (ISO3 standard)
        self.country_mapping = {
            'United States': 'USA', 'Germany': 'DEU', 'Japan': 'JPN',
            'United Kingdom': 'GBR', 'France': 'FRA', 'Italy': 'ITA',
            'Canada': 'CAN', 'Australia': 'AUS', 'Switzerland': 'CHE',
            'Netherlands': 'NLD', 'Spain': 'ESP', 'Sweden': 'SWE',
            'Norway': 'NOR', 'Denmark': 'DNK', 'Belgium': 'BEL',
            'Austria': 'AUT', 'Finland': 'FIN', 'Ireland': 'IRL',
            'Portugal': 'PRT', 'Greece': 'GRC', 'Poland': 'POL',
            'Czech Republic': 'CZE', 'Hungary': 'HUN', 'Slovakia': 'SVK',
            'Slovenia': 'SVN', 'Estonia': 'EST', 'Latvia': 'LVA',
            'Lithuania': 'LTU', 'Bulgaria': 'BGR', 'Romania': 'ROU',
            'Croatia': 'HRV', 'Cyprus': 'CYP', 'Malta': 'MLT',
            'Luxembourg': 'LUX', 'Iceland': 'ISL', 'New Zealand': 'NZL',
            'South Korea': 'KOR', 'Singapore': 'SGP', 'Hong Kong': 'HKG',
            'Taiwan': 'TWN', 'Israel': 'ISR', 'South Africa': 'ZAF',
            'Brazil': 'BRA', 'Mexico': 'MEX', 'Argentina': 'ARG',
            'Chile': 'CHL', 'Colombia': 'COL', 'Peru': 'PER',
            'Uruguay': 'URY', 'India': 'IND', 'China': 'CHN',
            'Indonesia': 'IDN', 'Malaysia': 'MYS', 'Thailand': 'THA',
            'Philippines': 'PHL', 'Vietnam': 'VNM', 'Turkey': 'TUR',
            'Russia': 'RUS', 'Ukraine': 'UKR', 'Saudi Arabia': 'SAU',
            'United Arab Emirates': 'ARE', 'Qatar': 'QAT', 'Kuwait': 'KWT',
            'Egypt': 'EGY', 'Morocco': 'MAR', 'Nigeria': 'NGA',
            'Kenya': 'KEN', 'Ghana': 'GHA', 'Ethiopia': 'ETH'
        }
    
    def load_bond_yields(self):
        """Load real bond yield data"""
        print("📊 Loading bond yield data...")
        
        bond_data = pd.read_csv(self.processed_dir / 'real_merged_bond_yields.csv')
        bond_data['Date'] = pd.to_datetime(bond_data['Date'])
        
        # Filter to analysis period and add country codes
        bond_data = bond_data[bond_data['Date'] >= '1995-01-01']  # Start from 1995 for better coverage
        bond_data['iso3c'] = bond_data['Country'].map(self.country_mapping)
        
        # Resample to monthly frequency
        bond_data = bond_data.groupby(['iso3c', pd.Grouper(key='Date', freq='M')])['yield_rate'].mean().reset_index()
        bond_data.rename(columns={'yield_rate': 'bond_yield', 'Date': 'date'}, inplace=True)
        
        print(f"  ✅ Bond yields: {len(bond_data):,} records, {bond_data['iso3c'].nunique()} countries")
        return bond_data
    
    def load_nd_gain_data(self):
        """Load ND-GAIN vulnerability data"""
        print("📊 Loading ND-GAIN data...")
        
        nd_gain_file = self.external_dir / 'nd_gain_countryindex_2025' / 'resources' / 'vulnerability' / 'exposure.csv'
        
        if nd_gain_file.exists():
            nd_gain_data = pd.read_csv(nd_gain_file)
            
            # Reshape from wide to long format
            nd_gain_long = nd_gain_data.melt(
                id_vars=['ISO3', 'Name'], 
                var_name='year', 
                value_name='nd_gain'
            )
            
            # Convert to monthly frequency
            monthly_nd_gain = []
            for _, row in nd_gain_long.iterrows():
                year = int(row['year'])
                for month in range(1, 13):
                    monthly_nd_gain.append({
                        'iso3c': row['ISO3'],
                        'date': pd.Timestamp(year=year, month=month, day=1),
                        'nd_gain': row['nd_gain']
                    })
            
            nd_gain_monthly = pd.DataFrame(monthly_nd_gain)
            print(f"  ✅ ND-GAIN: {len(nd_gain_monthly):,} records, {nd_gain_monthly['iso3c'].nunique()} countries")
            return nd_gain_monthly
        else:
            print("  ❌ ND-GAIN data not found")
            return pd.DataFrame()
    
    def load_imf_cpi_data(self):
        """Load IMF CPI data for inflation"""
        print("📊 Loading IMF CPI data...")
        
        cpi_file = self.external_dir / 'Control data' / 'IMF CPI data.csv'
        
        if not cpi_file.exists():
            print("  ❌ IMF CPI data not found")
            return pd.DataFrame()
        
        cpi_data = pd.read_csv(cpi_file)
        
        # Filter for year-over-year inflation data
        inflation_data = cpi_data[
            cpi_data['TYPE_OF_TRANSFORMATION'].str.contains('Year-over-year', na=False)
        ]
        
        # Process the time series data
        processed_inflation = []
        
        for _, row in inflation_data.iterrows():
            country = row['COUNTRY']
            
            # Map country name to ISO3 code
            iso3c = None
            for country_name, code in self.country_mapping.items():
                if country_name.lower() in country.lower() or country.lower() in country_name.lower():
                    iso3c = code
                    break
            
            if iso3c is None:
                continue  # Skip if we can't map the country
            
            # Extract time series data (columns that look like dates)
            for col in cpi_data.columns:
                if col.startswith(('19', '20')) and 'M' in col:  # Monthly data
                    try:
                        # Parse date (format like "2020-M01")
                        year, month = col.split('-M')
                        date = pd.Timestamp(year=int(year), month=int(month), day=1)
                        
                        value = row[col]
                        if pd.notna(value) and value != '':
                            processed_inflation.append({
                                'iso3c': iso3c,
                                'date': date,
                                'inflation': float(value)
                            })
                    except:
                        continue
        
        inflation_df = pd.DataFrame(processed_inflation)
        if len(inflation_df) > 0:
            print(f"  ✅ Inflation: {len(inflation_df):,} records, {inflation_df['iso3c'].nunique()} countries")
        else:
            print("  ❌ No inflation data processed")
        
        return inflation_df
    
    def load_imf_weo_data(self):
        """Load IMF WEO data for macroeconomic controls"""
        print("📊 Loading IMF WEO data...")
        
        weo_file = self.external_dir / 'Control data' / 'IMF WEO data.csv'
        
        if not weo_file.exists():
            print("  ❌ IMF WEO data not found")
            return pd.DataFrame()
        
        weo_data = pd.read_csv(weo_file)
        
        # Target indicators
        target_indicators = {
            'unemployment': 'Unemployment rate',
            'government_debt': 'Gross debt, General government, Percent of GDP',
            'government_expenditure': 'Expenditure, General government, Percent of GDP'
        }
        
        processed_weo = []
        
        for variable, indicator_pattern in target_indicators.items():
            matching_data = weo_data[weo_data['INDICATOR'].str.contains(indicator_pattern, na=False)]
            
            for _, row in matching_data.iterrows():
                country = row['COUNTRY']
                
                # Map country name to ISO3 code
                iso3c = None
                for country_name, code in self.country_mapping.items():
                    if country_name.lower() in country.lower() or country.lower() in country_name.lower():
                        iso3c = code
                        break
                
                if iso3c is None:
                    continue
                
                # Extract time period and value
                time_period = row['TIME_PERIOD']
                value = row['OBS_VALUE']
                
                if pd.notna(value) and pd.notna(time_period):
                    try:
                        # Parse time period (could be yearly like "2020")
                        year = int(float(time_period))
                        
                        # Create monthly data (forward fill annual data)
                        for month in range(1, 13):
                            date = pd.Timestamp(year=year, month=month, day=1)
                            processed_weo.append({
                                'iso3c': iso3c,
                                'date': date,
                                variable: float(value)
                            })
                    except:
                        continue
        
        if processed_weo:
            weo_df = pd.DataFrame(processed_weo)
            # Aggregate by iso3c and date (in case of duplicates)
            weo_df = weo_df.groupby(['iso3c', 'date']).mean().reset_index()
            print(f"  ✅ WEO data: {len(weo_df):,} records, {weo_df['iso3c'].nunique()} countries")
            return weo_df
        else:
            print("  ❌ No WEO data processed")
            return pd.DataFrame()
    
    def load_wgi_data(self):
        """Load World Governance Indicators"""
        print("📊 Loading World Governance Indicators...")
        
        wgi_file = self.external_dir / 'Control data' / 'wgidataset_excel' / 'wgidataset.xlsx'
        
        if not wgi_file.exists():
            print("  ❌ WGI data not found")
            return pd.DataFrame()
        
        try:
            wgi_data = pd.read_excel(wgi_file)
            
            # Process WGI data
            processed_wgi = []
            
            # Indicator mapping
            wgi_indicators = {
                'control_corruption': 'cc',
                'government_effectiveness': 'ge',
                'political_stability': 'pv',
                'regulatory_quality': 'rq',
                'rule_of_law': 'rl',
                'voice_accountability': 'va'
            }
            
            for _, row in wgi_data.iterrows():
                iso3c = row['code']
                year = row['year']
                indicator = row['indicator']
                estimate = row['estimate']
                
                if pd.notna(estimate) and indicator in wgi_indicators.values():
                    # Find the variable name
                    variable_name = None
                    for var_name, indicator_code in wgi_indicators.items():
                        if indicator_code == indicator:
                            variable_name = var_name
                            break
                    
                    if variable_name:
                        # Create monthly data (forward fill annual data)
                        for month in range(1, 13):
                            date = pd.Timestamp(year=year, month=month, day=1)
                            processed_wgi.append({
                                'iso3c': iso3c,
                                'date': date,
                                variable_name: float(estimate)
                            })
            
            if processed_wgi:
                wgi_df = pd.DataFrame(processed_wgi)
                # Aggregate by iso3c, date, and variable
                wgi_df = wgi_df.groupby(['iso3c', 'date']).mean().reset_index()
                print(f"  ✅ WGI data: {len(wgi_df):,} records, {wgi_df['iso3c'].nunique()} countries")
                return wgi_df
            else:
                print("  ❌ No WGI data processed")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"  ❌ Error loading WGI data: {e}")
            return pd.DataFrame()
    
    def create_comprehensive_dataset(self):
        """Create the comprehensive merged dataset"""
        print("\n🔄 Creating comprehensive dataset...")
        
        # Load all data sources
        bond_yields = self.load_bond_yields()
        nd_gain = self.load_nd_gain_data()
        inflation = self.load_imf_cpi_data()
        weo_data = self.load_imf_weo_data()
        wgi_data = self.load_wgi_data()
        
        # Start with bond yields as base
        merged = bond_yields.copy()
        
        # Merge each dataset
        datasets_to_merge = [
            (nd_gain, "ND-GAIN"),
            (inflation, "Inflation"),
            (weo_data, "WEO"),
            (wgi_data, "WGI")
        ]
        
        for dataset, name in datasets_to_merge:
            if len(dataset) > 0:
                print(f"  🔗 Merging {name} data...")
                merged = merged.merge(dataset, on=['iso3c', 'date'], how='left')
            else:
                print(f"  ⏭️ Skipping {name} data (empty)")
        
        # Add region information
        region_mapping = {
            'USA': 'North America', 'CAN': 'North America', 'MEX': 'North America',
            'BRA': 'South America', 'ARG': 'South America', 'CHL': 'South America',
            'COL': 'South America', 'PER': 'South America', 'URY': 'South America',
            'DEU': 'Europe', 'FRA': 'Europe', 'ITA': 'Europe', 'GBR': 'Europe',
            'ESP': 'Europe', 'NLD': 'Europe', 'CHE': 'Europe', 'SWE': 'Europe',
            'NOR': 'Europe', 'DNK': 'Europe', 'BEL': 'Europe', 'AUT': 'Europe',
            'FIN': 'Europe', 'IRL': 'Europe', 'PRT': 'Europe', 'GRC': 'Europe',
            'POL': 'Europe', 'CZE': 'Europe', 'HUN': 'Europe', 'SVK': 'Europe',
            'SVN': 'Europe', 'EST': 'Europe', 'LVA': 'Europe', 'LTU': 'Europe',
            'BGR': 'Europe', 'ROU': 'Europe', 'HRV': 'Europe', 'CYP': 'Europe',
            'MLT': 'Europe', 'LUX': 'Europe', 'ISL': 'Europe', 'RUS': 'Europe',
            'UKR': 'Europe', 'TUR': 'Asia', 'JPN': 'Asia', 'KOR': 'Asia',
            'CHN': 'Asia', 'IND': 'Asia', 'IDN': 'Asia', 'MYS': 'Asia',
            'THA': 'Asia', 'PHL': 'Asia', 'VNM': 'Asia', 'SGP': 'Asia',
            'HKG': 'Asia', 'TWN': 'Asia', 'ISR': 'Middle East', 'SAU': 'Middle East',
            'ARE': 'Middle East', 'QAT': 'Middle East', 'KWT': 'Middle East',
            'EGY': 'Africa', 'MAR': 'Africa', 'NGA': 'Africa', 'KEN': 'Africa',
            'GHA': 'Africa', 'ETH': 'Africa', 'ZAF': 'Africa', 'AUS': 'Oceania',
            'NZL': 'Oceania'
        }
        
        merged['region'] = merged['iso3c'].map(region_mapping)
        
        # Sort and clean
        merged = merged.sort_values(['iso3c', 'date']).reset_index(drop=True)
        
        # Save comprehensive dataset
        output_path = self.data_dir / 'comprehensive_real_panel.csv'
        merged.to_csv(output_path, index=False)
        
        print(f"\n✅ Comprehensive dataset created:")
        print(f"   📁 Location: {output_path}")
        print(f"   📊 Shape: {merged.shape}")
        print(f"   🌍 Countries: {merged['iso3c'].nunique()}")
        print(f"   📅 Date range: {merged['date'].min()} to {merged['date'].max()}")
        print(f"   📈 Variables: {list(merged.columns)}")
        
        # Data quality summary
        print(f"\n📋 Data Quality Summary:")
        missing_summary = merged.isnull().sum()
        for col in merged.columns:
            if col not in ['iso3c', 'date', 'region']:
                missing_pct = (missing_summary[col] / len(merged)) * 100
                print(f"   {col}: {missing_pct:.1f}% missing")
        
        return merged
    
    def create_analysis_ready_dataset(self, merged_data):
        """Create analysis-ready dataset with complete cases"""
        print(f"\n🎯 Creating analysis-ready dataset...")
        
        # Define core variables for analysis
        core_vars = ['bond_yield', 'nd_gain']
        
        # Add available control variables
        control_vars = []
        potential_controls = ['inflation', 'unemployment', 'government_debt', 
                            'government_expenditure', 'control_corruption', 
                            'government_effectiveness', 'rule_of_law']
        
        for var in potential_controls:
            if var in merged_data.columns:
                control_vars.append(var)
        
        analysis_vars = core_vars + control_vars + ['iso3c', 'date', 'region']
        
        # Create analysis dataset with complete cases
        analysis_data = merged_data[analysis_vars].dropna()
        
        # Save analysis-ready dataset
        analysis_path = self.data_dir / 'analysis_ready_panel.csv'
        analysis_data.to_csv(analysis_path, index=False)
        
        print(f"✅ Analysis-ready dataset created:")
        print(f"   📁 Location: {analysis_path}")
        print(f"   📊 Shape: {analysis_data.shape}")
        print(f"   🌍 Countries: {analysis_data['iso3c'].nunique()}")
        print(f"   📅 Date range: {analysis_data['date'].min()} to {analysis_data['date'].max()}")
        print(f"   📈 Core variables: {core_vars}")
        print(f"   📈 Control variables: {control_vars}")
        
        return analysis_data

def main():
    """Main integration function"""
    print("🚀 COMPREHENSIVE REAL DATA INTEGRATION")
    print("=" * 60)
    
    integrator = ComprehensiveDataIntegrator()
    
    # Create comprehensive dataset
    merged_data = integrator.create_comprehensive_dataset()
    
    # Create analysis-ready dataset
    analysis_data = integrator.create_analysis_ready_dataset(merged_data)
    
    print("\n" + "="*60)
    print("✅ COMPREHENSIVE DATA INTEGRATION COMPLETED!")
    print("="*60)
    
    print(f"\n📊 FINAL SUMMARY:")
    print(f"   Comprehensive dataset: {merged_data.shape[0]:,} observations")
    print(f"   Analysis-ready dataset: {analysis_data.shape[0]:,} observations")
    print(f"   Countries: {analysis_data['iso3c'].nunique()}")
    print(f"   Real control variables: {len([col for col in analysis_data.columns if col not in ['iso3c', 'date', 'region', 'bond_yield', 'nd_gain']])}")
    
    return analysis_data

if __name__ == "__main__":
    main()