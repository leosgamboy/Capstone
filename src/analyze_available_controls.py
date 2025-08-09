#!/usr/bin/env python3
"""
Comprehensive Analysis of Available Control Variables

This script analyzes all available real data sources to identify
which control variables we can extract for the thesis analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path

class ControlDataAnalyzer:
    def __init__(self):
        self.data_dir = Path('data/external/Data/Control data')
        self.available_controls = {}
        self.missing_controls = []
        
        # Target control variables for thesis
        self.target_controls = {
            'Core Macroeconomic Controls': [
                'Real GDP growth (monthly or annualized)',
                'Inflation rate or consumer price index',
                'Unemployment rate or output gap',
                'Current‑account balance (% of GDP)',
                'Fiscal balance or government primary deficit',
                'Public debt‑to‑GDP ratio'
            ],
            'Financial and Risk Controls': [
                'Sovereign credit rating (e.g., Moody\'s/S&P/Fitch)',
                'Sovereign CDS spread (basis points)',
                'Short‑term policy rate or benchmark risk‑free rate',
                'Exchange rate index or terms‑of‑trade'
            ],
            'Governance Controls': [
                'Democracy Index',
                'Government reliability data',
                'Corruption index'
            ]
        }
    
    def analyze_imf_cpi_data(self):
        """Analyze IMF CPI data for inflation controls"""
        print("🔍 Analyzing IMF CPI Data...")
        
        cpi_file = self.data_dir / 'IMF CPI data.csv'
        if not cpi_file.exists():
            print("❌ IMF CPI data not found")
            return
        
        cpi_data = pd.read_csv(cpi_file)
        
        print(f"  📊 Shape: {cpi_data.shape}")
        print(f"  🌍 Countries: {cpi_data['COUNTRY'].nunique()}")
        print(f"  📅 Time columns: {len([col for col in cpi_data.columns if col.startswith(('19', '20'))])} time periods")
        
        # Check transformation types for inflation data
        transformations = cpi_data['TYPE_OF_TRANSFORMATION'].unique()
        print(f"  📈 Transformations available: {transformations}")
        
        # Look for year-over-year percent change (inflation)
        inflation_data = cpi_data[cpi_data['TYPE_OF_TRANSFORMATION'].str.contains('Year-over-year', na=False)]
        print(f"  🎯 Inflation data (YoY): {len(inflation_data)} series")
        
        if len(inflation_data) > 0:
            self.available_controls['Inflation rate (CPI YoY)'] = {
                'source': 'IMF CPI data',
                'countries': inflation_data['COUNTRY'].nunique(),
                'series_count': len(inflation_data),
                'frequency': inflation_data['FREQUENCY'].unique().tolist(),
                'quality': 'HIGH - Real IMF data'
            }
    
    def analyze_imf_weo_data(self):
        """Analyze IMF WEO data for macroeconomic controls"""
        print("\n🔍 Analyzing IMF WEO Data...")
        
        weo_file = self.data_dir / 'IMF WEO data.csv'
        if not weo_file.exists():
            print("❌ IMF WEO data not found")
            return
        
        weo_data = pd.read_csv(weo_file)
        
        print(f"  📊 Shape: {weo_data.shape}")
        print(f"  🌍 Countries: {weo_data['COUNTRY'].nunique()}")
        
        # Map WEO indicators to our target controls
        weo_mapping = {
            'GDP growth': 'Gross domestic product (GDP), Constant prices, Percent change',
            'Unemployment rate': 'Unemployment rate',
            'Current account balance': 'Current account balance (credit less debit), Percent of GDP',
            'Government debt': 'Gross debt, General government, Percent of GDP',
            'Government expenditure': 'Expenditure, General government, Percent of GDP'
        }
        
        for control_name, indicator_pattern in weo_mapping.items():
            matching_indicators = weo_data[weo_data['INDICATOR'].str.contains(indicator_pattern, na=False)]
            
            if len(matching_indicators) > 0:
                countries_with_data = matching_indicators['COUNTRY'].nunique()
                print(f"  ✅ {control_name}: {countries_with_data} countries")
                
                self.available_controls[control_name] = {
                    'source': 'IMF WEO data',
                    'countries': countries_with_data,
                    'indicator': indicator_pattern,
                    'quality': 'HIGH - Real IMF data'
                }
            else:
                print(f"  ❌ {control_name}: Not found")
    
    def analyze_wgi_data(self):
        """Analyze World Governance Indicators data"""
        print("\n🔍 Analyzing World Governance Indicators...")
        
        wgi_file = self.data_dir / 'wgidataset_excel' / 'wgidataset.xlsx'
        if not wgi_file.exists():
            print("❌ WGI data not found")
            return
        
        try:
            wgi_data = pd.read_excel(wgi_file)
            
            print(f"  📊 Shape: {wgi_data.shape}")
            print(f"  🌍 Countries: {wgi_data['countryname'].nunique()}")
            print(f"  📅 Years: {wgi_data['year'].min()} to {wgi_data['year'].max()}")
            
            # Check available governance indicators
            indicators = wgi_data['indicator'].unique()
            print(f"  📈 Available indicators: {indicators}")
            
            # Map to our target governance controls
            governance_mapping = {
                'Government Effectiveness': 'ge',
                'Regulatory Quality': 'rq', 
                'Rule of Law': 'rl',
                'Control of Corruption': 'cc',
                'Voice and Accountability': 'va',
                'Political Stability': 'pv'
            }
            
            for control_name, indicator_code in governance_mapping.items():
                matching_data = wgi_data[wgi_data['indicator'] == indicator_code]
                
                if len(matching_data) > 0:
                    countries_with_data = matching_data['countryname'].nunique()
                    print(f"  ✅ {control_name}: {countries_with_data} countries")
                    
                    self.available_controls[control_name] = {
                        'source': 'World Governance Indicators',
                        'countries': countries_with_data,
                        'years': f"{matching_data['year'].min()}-{matching_data['year'].max()}",
                        'quality': 'HIGH - World Bank governance data'
                    }
                else:
                    print(f"  ❌ {control_name}: Not found")
                    
        except Exception as e:
            print(f"  ❌ Error reading WGI data: {e}")
    
    def identify_missing_controls(self):
        """Identify which controls are missing and need alternative sources"""
        print("\n🔍 Identifying Missing Controls...")
        
        # Check which target controls we don't have
        all_targets = []
        for category, controls in self.target_controls.items():
            all_targets.extend(controls)
        
        available_keys = set(self.available_controls.keys())
        
        # Manual mapping of what we found to target controls
        found_controls = {
            'Real GDP growth (monthly or annualized)': 'GDP growth' in available_keys,
            'Inflation rate or consumer price index': 'Inflation rate (CPI YoY)' in available_keys,
            'Unemployment rate or output gap': 'Unemployment rate' in available_keys,
            'Current‑account balance (% of GDP)': 'Current account balance' in available_keys,
            'Fiscal balance or government primary deficit': 'Government expenditure' in available_keys,  # Proxy
            'Public debt‑to‑GDP ratio': 'Government debt' in available_keys,
            'Sovereign credit rating (e.g., Moody\'s/S&P/Fitch)': False,
            'Sovereign CDS spread (basis points)': False,
            'Short‑term policy rate or benchmark risk‑free rate': False,
            'Exchange rate index or terms‑of‑trade': False,
            'Democracy Index': 'Voice and Accountability' in available_keys,  # Proxy
            'Government reliability data': 'Government Effectiveness' in available_keys,
            'Corruption index': 'Control of Corruption' in available_keys
        }
        
        print("\n📋 CONTROL VARIABLE ASSESSMENT:")
        print("=" * 60)
        
        for category, controls in self.target_controls.items():
            print(f"\n{category}:")
            for control in controls:
                status = "✅ AVAILABLE" if found_controls.get(control, False) else "❌ MISSING"
                print(f"  {status}: {control}")
                
                if not found_controls.get(control, False):
                    self.missing_controls.append(control)
    
    def generate_data_integration_strategy(self):
        """Generate strategy for integrating available real data"""
        print("\n🚀 DATA INTEGRATION STRATEGY:")
        print("=" * 60)
        
        print("\n✅ AVAILABLE REAL DATA (HIGH PRIORITY):")
        for control, details in self.available_controls.items():
            print(f"  • {control}")
            print(f"    Source: {details['source']}")
            print(f"    Countries: {details['countries']}")
            print(f"    Quality: {details['quality']}")
        
        print(f"\n❌ MISSING CONTROLS ({len(self.missing_controls)} items):")
        for control in self.missing_controls:
            print(f"  • {control}")
        
        print("\n💡 RECOMMENDATIONS FOR 10-DAY TIMELINE:")
        print("1. 🎯 FOCUS ON AVAILABLE REAL DATA:")
        print("   - Use IMF WEO for: GDP growth, unemployment, current account, debt")
        print("   - Use IMF CPI for: Inflation rates")
        print("   - Use WGI for: Governance indicators (corruption, effectiveness)")
        
        print("\n2. 🔄 QUICK SOLUTIONS FOR MISSING DATA:")
        print("   - Credit ratings: Use simplified categorical approach or exclude")
        print("   - CDS spreads: Use bond yield spreads as proxy or exclude")
        print("   - Policy rates: Use central bank data for major countries only")
        print("   - Exchange rates: Focus on major currencies or exclude")
        
        print("\n3. 📊 ANALYSIS APPROACH:")
        print("   - Primary model: Bond yields ~ ND-GAIN + Available real controls")
        print("   - Robustness: Test with different control combinations")
        print("   - Subgroup analysis: Focus on countries with complete data")
    
    def run_complete_analysis(self):
        """Run the complete control data analysis"""
        print("🔍 COMPREHENSIVE CONTROL DATA ANALYSIS")
        print("=" * 60)
        
        # Analyze each data source
        self.analyze_imf_cpi_data()
        self.analyze_imf_weo_data()
        self.analyze_wgi_data()
        
        # Identify gaps
        self.identify_missing_controls()
        
        # Generate strategy
        self.generate_data_integration_strategy()
        
        return self.available_controls, self.missing_controls

def main():
    """Main analysis function"""
    analyzer = ControlDataAnalyzer()
    available, missing = analyzer.run_complete_analysis()
    
    print(f"\n📊 SUMMARY:")
    print(f"  Available controls: {len(available)}")
    print(f"  Missing controls: {len(missing)}")
    print(f"  Coverage: {len(available)/(len(available)+len(missing))*100:.1f}%")

if __name__ == "__main__":
    main()