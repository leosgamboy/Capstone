#!/usr/bin/env python3
"""
Real Yield Data Integration Script

This script reads and processes the actual bond yield data from the "Yield data real" folder,
replacing the sample data with real historical bond yield data.

Features:
- Reads all CSV files from the yield data real folder
- Processes real historical bond yield data
- Creates a comprehensive real dataset
- Handles different file formats and structures
- Generates summary statistics for real data
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class RealYieldDataIntegrator:
    def __init__(self, data_dir="data/external/Data/Yield data/Yield data real "):
        self.data_dir = data_dir
        self.merged_data = None
        
        # Comprehensive country mapping based on the actual file names
        self.country_mapping = {
            'IGUSA': 'United States',
            'IGJPN': 'Japan', 
            'IGGBR': 'United Kingdom',
            'IGDEU': 'Germany',
            'IGFRA': 'France',
            'IGITA': 'Italy',
            'IGESP': 'Spain',
            'IGCAN': 'Canada',
            'IGAUS': 'Australia',
            'IGCHE': 'Switzerland',
            'IGSWE': 'Sweden',
            'IGNLD': 'Netherlands',
            'IGBEL': 'Belgium',
            'IGAUT': 'Austria',
            'IGFIN': 'Finland',
            'IGDNK': 'Denmark',
            'IGNOR': 'Norway',
            'IGIRL': 'Ireland',
            'IGPRT': 'Portugal',
            'IGGRC': 'Greece',
            'IGLUX': 'Luxembourg',
            'IGCZE': 'Czech Republic',
            'IGPOL': 'Poland',
            'IGHUN': 'Hungary',
            'IGSVK': 'Slovakia',
            'IGSVN': 'Slovenia',
            'IGHRV': 'Croatia',
            'IGLVA': 'Latvia',
            'IGLTU': 'Lithuania',
            'IGBGR': 'Bulgaria',
            'IGROU': 'Romania',
            'IGARM': 'Armenia',
            'IGSRB': 'Serbia',
            'IGRUS': 'Russia',
            'IGTUR': 'Turkey',
            'IGISR': 'Israel',
            'IGEGY': 'Egypt',
            'IGQAT': 'Qatar',
            'IGUGA': 'Uganda',
            'IGKEN': 'Kenya',
            'IGZMB': 'Zambia',
            'IGBWA': 'Botswana',
            'IGNAM': 'Namibia',
            'IGZAF': 'South Africa',
            'IGBRA': 'Brazil',
            'IGARG': 'Argentina',
            'IGCHL': 'Chile',
            'IGPER': 'Peru',
            'IGCOL': 'Colombia',
            'IGCHN': 'China',
            'IGKOR': 'South Korea',
            'IGTWN': 'Taiwan',
            'IGHKG': 'Hong Kong',
            'IGSGP': 'Singapore',
            'IGMYS': 'Malaysia',
            'IGTHA': 'Thailand',
            'IGIDN': 'Indonesia',
            'IGPHL': 'Philippines',
            'IGVNM': 'Vietnam',
            'IGBGD': 'Bangladesh',
            'IGPAK': 'Pakistan',
            'IGIND': 'India',
            'IGLKA': 'Sri Lanka',
            'IGCYP': 'Cyprus',
            'IGMLT': 'Malta',
            'IGMEX': 'Mexico',
            'IGNZL': 'New Zealand',
            'IGISL': 'Iceland',
            'IGLIE': 'Liechtenstein',
            'IGMCO': 'Monaco',
            'IGSMR': 'San Marino',
            'IGVAT': 'Vatican City',
            'IGAND': 'Andorra',
            'IGCIV': 'Ivory Coast',
            'IGNGN': 'Nigeria',
            'IGGHA': 'Ghana',
            'IGSEN': 'Senegal',
            'IGTUN': 'Tunisia',
            'IGMAR': 'Morocco',
            'IGALG': 'Algeria',
            'IGLBY': 'Libya',
            'IGSDN': 'Sudan',
            'IGETH': 'Ethiopia',
            'IGSOM': 'Somalia',
            'IGDJI': 'Djibouti',
            'IGERI': 'Eritrea',
            'IGSLE': 'Sierra Leone',
            'IGLBR': 'Liberia',
            'IGGIN': 'Guinea',
            'IGGMB': 'Gambia',
            'IGMLI': 'Mali',
            'IGBFA': 'Burkina Faso',
            'IGNER': 'Niger',
            'IGTCD': 'Chad',
            'IGCMR': 'Cameroon',
            'IGGAB': 'Gabon',
            'IGCOG': 'Congo',
            'IGCOD': 'DR Congo',
            'IGCAF': 'Central African Republic',
            'IGEUR': 'Euro Area',
            'IGUSAI': 'United States (Inflation)',
            'IGAUSI': 'Australia (Inflation)',
            'IGGBRI': 'United Kingdom (Inflation)',
            'IGNORG': 'Norway (Government)',
            'EUF0010DEU': 'Germany (Euro)',
            'EUF0110DEU': 'Germany (Euro)',
            'EUF0210DEU': 'Germany (Euro)',
            'EUF0310DEU': 'Germany (Euro)'
        }
        
        # Group countries by region for analysis
        self.region_mapping = {
            'North America': ['United States', 'Canada'],
            'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands', 
                      'Belgium', 'Austria', 'Finland', 'Denmark', 'Norway', 'Ireland', 'Portugal',
                      'Greece', 'Luxembourg', 'Czech Republic', 'Poland', 'Hungary', 'Slovakia',
                      'Slovenia', 'Croatia', 'Latvia', 'Lithuania', 'Bulgaria', 'Romania',
                      'Armenia', 'Serbia', 'Cyprus', 'Malta', 'Iceland', 'Liechtenstein',
                      'Monaco', 'San Marino', 'Vatican City', 'Andorra'],
            'Asia Pacific': ['Japan', 'Australia', 'China', 'South Korea', 'Taiwan', 'Hong Kong',
                           'Singapore', 'Malaysia', 'Thailand', 'Indonesia', 'Philippines',
                           'Vietnam', 'Bangladesh', 'Pakistan', 'India', 'Sri Lanka', 'New Zealand'],
            'Emerging Markets': ['Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia', 'Mexico',
                               'Russia', 'Turkey', 'South Africa', 'Egypt', 'Qatar'],
            'Africa': ['Uganda', 'Kenya', 'Zambia', 'Botswana', 'Namibia', 'South Africa'],
            'Middle East': ['Israel', 'Egypt', 'Qatar', 'Turkey']
        }
    
    def get_country_from_filename(self, filename):
        """Extract country name from filename"""
        base_name = os.path.splitext(filename)[0]
        
        for code, country in self.country_mapping.items():
            if base_name.startswith(code):
                return country, code
        
        # If no match found, return the base name as country
        return base_name, base_name
    
    def load_single_real_file(self, file_path):
        """Load a single real yield data file"""
        try:
            filename = os.path.basename(file_path)
            country, country_code = self.get_country_from_filename(filename)
            
            print(f"Loading {filename} for {country}...")
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Find where the actual data starts (after metadata)
            data_start = None
            for i, row in df.iterrows():
                if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip():
                    try:
                        # Try to parse as date
                        pd.to_datetime(str(row.iloc[0]), format='%m/%d/%Y', errors='coerce')
                        data_start = i
                        break
                    except:
                        continue
            
            if data_start is None:
                print(f"Could not find data start in {filename}")
                return None
            
            # Read the data starting from the identified row
            df = pd.read_csv(file_path, skiprows=data_start)
            
            # Handle the column mismatch issue
            if len(df.columns) == 6:
                df.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close']
            elif len(df.columns) >= 2:
                # Use only the first 6 columns if we have more
                df = df.iloc[:, :6]
                df.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close']
            else:
                # Fallback for other cases
                df.columns = ['Date', 'Ticker'] + [f'Col_{i}' for i in range(len(df.columns)-2)]
            
            # Clean up the data
            df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')
            df = df.dropna(subset=['Date'])
            
            # Use Close price as yield if available
            if 'Close' in df.columns:
                df['yield_rate'] = pd.to_numeric(df['Close'], errors='coerce')
            else:
                # Use the last numeric column
                for col in reversed(df.columns):
                    if col not in ['Date', 'Ticker']:
                        df['yield_rate'] = pd.to_numeric(df[col], errors='coerce')
                        break
            
            df = df.dropna(subset=['yield_rate'])
            
            # Add country info
            df['Country_Code'] = country_code
            df['Country'] = country
            df['RIC'] = f"{country_code}10YT=RR"
            df['source'] = f"real_gfd_{country_code.lower()}"
            
            # Select relevant columns
            df = df[['Date', 'RIC', 'yield_rate', 'Country_Code', 'Country', 'source']]
            
            print(f"Loaded {len(df)} records from {country} ({df['Date'].min()} to {df['Date'].max()})")
            return df
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def load_all_real_files(self):
        """Load all real yield data files from the directory"""
        print("Loading all real yield data files...")
        
        if not os.path.exists(self.data_dir):
            print(f"Directory not found: {self.data_dir}")
            return None
        
        # Get all CSV files
        csv_files = glob.glob(os.path.join(self.data_dir, "*.csv"))
        print(f"Found {len(csv_files)} CSV files")
        
        all_dataframes = []
        
        for file_path in csv_files:
            df = self.load_single_real_file(file_path)
            if df is not None and len(df) > 0:
                all_dataframes.append(df)
        
        if not all_dataframes:
            print("No data loaded!")
            return None
        
        # Merge all data
        self.merged_data = pd.concat(all_dataframes, ignore_index=True)
        
        # Remove duplicates based on Date, Country_Code, and RIC
        self.merged_data = self.merged_data.drop_duplicates(
            subset=['Date', 'Country_Code', 'RIC'], 
            keep='first'
        )
        
        # Sort by date and country
        self.merged_data = self.merged_data.sort_values(['Date', 'Country_Code'])
        
        print(f"Merged dataset contains {len(self.merged_data)} records")
        print(f"Countries: {self.merged_data['Country'].nunique()}")
        print(f"Date range: {self.merged_data['Date'].min()} to {self.merged_data['Date'].max()}")
        
        return self.merged_data
    
    def clean_real_data(self):
        """Clean the merged real dataset"""
        print("Cleaning merged real dataset...")
        
        if self.merged_data is None:
            print("No data to clean!")
            return None
        
        # Remove outliers (yields > 50% or < -5%)
        initial_count = len(self.merged_data)
        self.merged_data = self.merged_data[
            (self.merged_data['yield_rate'] >= -5) & 
            (self.merged_data['yield_rate'] <= 50)
        ]
        outliers_removed = initial_count - len(self.merged_data)
        print(f"Removed {outliers_removed} outlier records")
        
        # Ensure date format is consistent
        self.merged_data['Date'] = pd.to_datetime(self.merged_data['Date'])
        
        # Add year and month columns for analysis
        self.merged_data['Year'] = self.merged_data['Date'].dt.year
        self.merged_data['Month'] = self.merged_data['Date'].dt.month
        self.merged_data['Quarter'] = self.merged_data['Date'].dt.quarter
        
        # Add decade column for long-term analysis
        self.merged_data['Decade'] = (self.merged_data['Year'] // 10) * 10
        
        # Add region information
        self.merged_data['Region'] = self.merged_data['Country'].apply(self.get_region)
        
        print(f"Cleaned dataset contains {len(self.merged_data)} records")
        return self.merged_data
    
    def get_region(self, country):
        """Get region for a country"""
        for region, countries in self.region_mapping.items():
            if country in countries:
                return region
        return 'Other'
    
    def generate_real_summary_stats(self):
        """Generate summary statistics for the real merged dataset"""
        print("Generating summary statistics for real data...")
        
        if self.merged_data is None:
            print("No data to analyze!")
            return
        
        # Basic statistics
        print("\n=== REAL YIELD DATA SUMMARY ===")
        print(f"Total records: {len(self.merged_data):,}")
        print(f"Date range: {self.merged_data['Date'].min()} to {self.merged_data['Date'].max()}")
        print(f"Countries: {self.merged_data['Country'].nunique()}")
        print(f"Data sources: {self.merged_data['source'].nunique()}")
        
        # Countries summary
        print("\n=== COUNTRIES SUMMARY ===")
        country_summary = self.merged_data.groupby('Country').agg({
            'yield_rate': ['count', 'mean', 'std', 'min', 'max'],
            'Date': ['min', 'max']
        }).round(2)
        print(country_summary)
        
        # Regional analysis
        print("\n=== REGIONAL ANALYSIS ===")
        regional_stats = self.merged_data.groupby('Region').agg({
            'yield_rate': ['count', 'mean', 'std', 'min', 'max'],
            'Country': 'nunique'
        }).round(3)
        print(regional_stats)
        
        # Time period summary
        print("\n=== TIME PERIOD SUMMARY ===")
        decade_summary = self.merged_data.groupby('Decade').agg({
            'yield_rate': ['count', 'mean', 'std'],
            'Country': 'nunique'
        }).round(2)
        print(decade_summary)
        
        return {
            'country_summary': country_summary,
            'regional_stats': regional_stats,
            'decade_summary': decade_summary
        }
    
    def save_real_data(self, output_path="data/processed/real_merged_bond_yields.csv"):
        """Save the real merged and cleaned dataset"""
        print(f"Saving real merged data to {output_path}...")
        
        if self.merged_data is None:
            print("No data to save!")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the data
        self.merged_data.to_csv(output_path, index=False)
        print(f"Real data saved successfully!")
        
        # Also save a summary file
        summary_path = output_path.replace('.csv', '_summary.txt')
        with open(summary_path, 'w') as f:
            f.write("REAL BOND YIELD DATA MERGE SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated on: {datetime.now()}\n")
            f.write(f"Total records: {len(self.merged_data):,}\n")
            f.write(f"Date range: {self.merged_data['Date'].min()} to {self.merged_data['Date'].max()}\n")
            f.write(f"Countries: {self.merged_data['Country'].nunique()}\n")
            f.write(f"Data sources: {self.merged_data['source'].nunique()}\n\n")
            
            f.write("COUNTRY SUMMARY:\n")
            f.write("-" * 30 + "\n")
            country_stats = self.merged_data.groupby('Country').agg({
                'yield_rate': ['count', 'mean', 'std', 'min', 'max']
            }).round(2)
            f.write(str(country_stats))
        
        print(f"Summary saved to {summary_path}")
    
    def run_real_data_pipeline(self):
        """Run the complete real data integration pipeline"""
        print("=" * 70)
        print("REAL YIELD DATA INTEGRATION PIPELINE")
        print("=" * 70)
        
        # Step 1: Load all real data
        merged_data = self.load_all_real_files()
        
        if merged_data is None:
            print("Pipeline failed: No real data could be loaded")
            return None
        
        # Step 2: Clean real data
        cleaned_data = self.clean_real_data()
        
        if cleaned_data is None:
            print("Pipeline failed: Real data cleaning failed")
            return None
        
        # Step 3: Generate summary statistics
        summary_stats = self.generate_real_summary_stats()
        
        # Step 4: Save real data
        self.save_real_data()
        
        print("\n" + "=" * 70)
        print("REAL DATA INTEGRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        return self.merged_data

def main():
    """Main function to run the real yield data integration pipeline"""
    integrator = RealYieldDataIntegrator()
    merged_data = integrator.run_real_data_pipeline()
    
    if merged_data is not None:
        print(f"\nFinal real dataset shape: {merged_data.shape}")
        print(f"Available countries: {sorted(merged_data['Country'].unique())}")
        print(f"Data sources: {sorted(merged_data['source'].unique())}")
    else:
        print("Real data integration failed!")

if __name__ == "__main__":
    main() 