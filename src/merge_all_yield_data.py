#!/usr/bin/env python3
"""
Comprehensive Bond Yield Data Merging Script

This script merges ALL bond yield data from the "Yield data real" folder,
which contains data for many countries worldwide.

Features:
- Loads all CSV files from the yield data real folder
- Standardizes country codes and dates
- Creates a comprehensive merged dataset
- Handles different file formats and structures
- Generates summary statistics for all countries
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ComprehensiveBondDataMerger:
    def __init__(self, data_dir="data/external/Data/Yield data/Yield data real"):
        self.data_dir = data_dir
        self.merged_data = None
        
        # Country code mapping based on file names
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
            'IGNGN': 'Nigeria',
            'IGGHA': 'Ghana',
            'IGCIV': 'Ivory Coast',
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
            'IGSEN': 'Senegal',
            'IGMLI': 'Mali',
            'IGBFA': 'Burkina Faso',
            'IGNER': 'Niger',
            'IGTCD': 'Chad',
            'IGCMR': 'Cameroon',
            'IGGAB': 'Gabon',
            'IGCOG': 'Congo',
            'IGCOD': 'DR Congo',
            'IGCAF': 'Central African Republic',
            'IGTCD': 'Chad',
            'IGNGA': 'Nigeria',
            'IGGHA': 'Ghana',
            'IGCIV': 'Ivory Coast',
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
            'IGSEN': 'Senegal',
            'IGMLI': 'Mali',
            'IGBFA': 'Burkina Faso',
            'IGNER': 'Niger',
            'IGTCD': 'Chad',
            'IGCMR': 'Cameroon',
            'IGGAB': 'Gabon',
            'IGCOG': 'Congo',
            'IGCOD': 'DR Congo',
            'IGCAF': 'Central African Republic',
            'IGBRA': 'Brazil',
            'IGARG': 'Argentina',
            'IGCHL': 'Chile',
            'IGPER': 'Peru',
            'IGCOL': 'Colombia',
            'IGVEN': 'Venezuela',
            'IGECU': 'Ecuador',
            'IGBOL': 'Bolivia',
            'IGPRY': 'Paraguay',
            'IGURY': 'Uruguay',
            'IGGUY': 'Guyana',
            'IGSUR': 'Suriname',
            'IGCHN': 'China',
            'IGJPN': 'Japan',
            'IGKOR': 'South Korea',
            'IGTWN': 'Taiwan',
            'IGHKG': 'Hong Kong',
            'IGSGP': 'Singapore',
            'IGMYS': 'Malaysia',
            'IGTHA': 'Thailand',
            'IGIDN': 'Indonesia',
            'IGPHL': 'Philippines',
            'IGVNM': 'Vietnam',
            'IGLAO': 'Laos',
            'IGKHM': 'Cambodia',
            'IGMMR': 'Myanmar',
            'IGBGD': 'Bangladesh',
            'IGPAK': 'Pakistan',
            'IGIND': 'India',
            'IGLKA': 'Sri Lanka',
            'IGNPL': 'Nepal',
            'IGBTN': 'Bhutan',
            'IGMDV': 'Maldives',
            'IGAFG': 'Afghanistan',
            'IGIRN': 'Iran',
            'IGIRQ': 'Iraq',
            'IGSYR': 'Syria',
            'IGLBN': 'Lebanon',
            'IGJOR': 'Jordan',
            'IGPSE': 'Palestine',
            'IGISR': 'Israel',
            'IGCYP': 'Cyprus',
            'IGMLT': 'Malta',
            'IGGRC': 'Greece',
            'IGALB': 'Albania',
            'IGMKD': 'North Macedonia',
            'IGMNE': 'Montenegro',
            'IGBIH': 'Bosnia and Herzegovina',
            'IGHRV': 'Croatia',
            'IGSVN': 'Slovenia',
            'IGSVK': 'Slovakia',
            'IGCZE': 'Czech Republic',
            'IGPOL': 'Poland',
            'IGLTU': 'Lithuania',
            'IGLVA': 'Latvia',
            'IGEST': 'Estonia',
            'IGFIN': 'Finland',
            'IGSWE': 'Sweden',
            'IGNOR': 'Norway',
            'IGDNK': 'Denmark',
            'IGISL': 'Iceland',
            'IGIRL': 'Ireland',
            'IGGBR': 'United Kingdom',
            'IGFRA': 'France',
            'IGDEU': 'Germany',
            'IGITA': 'Italy',
            'IGESP': 'Spain',
            'IGPRT': 'Portugal',
            'IGBEL': 'Belgium',
            'IGNLD': 'Netherlands',
            'IGLUX': 'Luxembourg',
            'IGAUT': 'Austria',
            'IGCHE': 'Switzerland',
            'IGLIE': 'Liechtenstein',
            'IGMCO': 'Monaco',
            'IGSMR': 'San Marino',
            'IGVAT': 'Vatican City',
            'IGAND': 'Andorra',
            'IGUSA': 'United States',
            'IGCAN': 'Canada',
            'IGMEX': 'Mexico',
            'IGGTM': 'Guatemala',
            'IGBLZ': 'Belize',
            'IGSLV': 'El Salvador',
            'IGHND': 'Honduras',
            'IGNIC': 'Nicaragua',
            'IGCRI': 'Costa Rica',
            'IGPAN': 'Panama',
            'IGCUB': 'Cuba',
            'IGJAM': 'Jamaica',
            'IGHTI': 'Haiti',
            'IGDOM': 'Dominican Republic',
            'IGPRI': 'Puerto Rico',
            'IGBRB': 'Barbados',
            'IGTTO': 'Trinidad and Tobago',
            'IGGRD': 'Grenada',
            'IGLCA': 'Saint Lucia',
            'IGVCT': 'Saint Vincent and the Grenadines',
            'IGATG': 'Antigua and Barbuda',
            'IGDMA': 'Dominica',
            'IGSKN': 'Saint Kitts and Nevis',
            'IGAUS': 'Australia',
            'IGNZL': 'New Zealand',
            'IGFJI': 'Fiji',
            'IGPNG': 'Papua New Guinea',
            'IGSLB': 'Solomon Islands',
            'IGVUT': 'Vanuatu',
            'IGNCL': 'New Caledonia',
            'IGPYF': 'French Polynesia',
            'IGCOK': 'Cook Islands',
            'IGTON': 'Tonga',
            'IGWSM': 'Samoa',
            'IGKIR': 'Kiribati',
            'IGTUV': 'Tuvalu',
            'IGNRU': 'Nauru',
            'IGPLW': 'Palau',
            'IGFSM': 'Micronesia',
            'IGMHL': 'Marshall Islands',
            'IGNRU': 'Nauru',
            'IGTUV': 'Tuvalu',
            'IGKIR': 'Kiribati',
            'IGWSM': 'Samoa',
            'IGTON': 'Tonga',
            'IGCOK': 'Cook Islands',
            'IGPYF': 'French Polynesia',
            'IGNCL': 'New Caledonia',
            'IGVUT': 'Vanuatu',
            'IGSLB': 'Solomon Islands',
            'IGPNG': 'Papua New Guinea',
            'IGFJI': 'Fiji',
            'IGNZL': 'New Zealand',
            'IGAUS': 'Australia'
        }
        
    def get_country_from_filename(self, filename):
        """Extract country name from filename"""
        # Remove file extension and get the base name
        base_name = os.path.splitext(filename)[0]
        
        # Try to match with known patterns
        for code, country in self.country_mapping.items():
            if base_name.startswith(code):
                return country, code
        
        # If no match found, return the base name as country
        return base_name, base_name
    
    def load_single_file(self, file_path):
        """Load a single yield data file"""
        try:
            filename = os.path.basename(file_path)
            country, country_code = self.get_country_from_filename(filename)
            
            print(f"Loading {filename} for {country}...")
            
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Find where the actual data starts
            data_start = None
            for i, row in df.iterrows():
                if pd.notna(row.iloc[0]) and str(row.iloc[0]).strip():
                    try:
                        # Try to parse as date
                        pd.to_datetime(str(row.iloc[0]), format='%d/%m/%Y')
                        data_start = i
                        break
                    except:
                        continue
            
            if data_start is None:
                print(f"Could not find data start in {filename}")
                return None
            
            # Read the data starting from the identified row
            df = pd.read_csv(file_path, skiprows=data_start)
            
            # Standardize column names
            if len(df.columns) >= 6:
                df.columns = ['Date', 'Ticker', 'Open', 'High', 'Low', 'Close']
            elif len(df.columns) >= 2:
                df.columns = ['Date', 'Ticker'] + [f'Col_{i}' for i in range(len(df.columns)-2)]
            
            # Clean up the data
            df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
            df = df.dropna(subset=['Date'])
            
            # Use Close price as yield if available, otherwise use the last numeric column
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
            df['source'] = f"gfd_{country_code.lower()}"
            
            # Select relevant columns
            df = df[['Date', 'RIC', 'yield_rate', 'Country_Code', 'Country', 'source']]
            
            print(f"Loaded {len(df)} records from {country}")
            return df
            
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def load_all_yield_data(self):
        """Load all yield data files from the directory"""
        print("Loading all yield data files...")
        
        if not os.path.exists(self.data_dir):
            print(f"Directory not found: {self.data_dir}")
            return None
        
        # Get all CSV files
        csv_files = glob.glob(os.path.join(self.data_dir, "*.csv"))
        print(f"Found {len(csv_files)} CSV files")
        
        all_dataframes = []
        
        for file_path in csv_files:
            df = self.load_single_file(file_path)
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
    
    def clean_data(self):
        """Clean the merged dataset"""
        print("Cleaning merged dataset...")
        
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
        
        print(f"Cleaned dataset contains {len(self.merged_data)} records")
        return self.merged_data
    
    def generate_summary_stats(self):
        """Generate summary statistics for the merged dataset"""
        print("Generating summary statistics...")
        
        if self.merged_data is None:
            print("No data to analyze!")
            return
        
        # Basic statistics
        print("\n=== COMPREHENSIVE DATASET SUMMARY ===")
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
        
        # Data sources summary
        print("\n=== DATA SOURCES SUMMARY ===")
        source_summary = self.merged_data.groupby('source').agg({
            'yield_rate': ['count', 'mean', 'std'],
            'Country': 'nunique'
        }).round(2)
        print(source_summary)
        
        # Time period summary
        print("\n=== TIME PERIOD SUMMARY ===")
        decade_summary = self.merged_data.groupby('Decade').agg({
            'yield_rate': ['count', 'mean', 'std'],
            'Country': 'nunique'
        }).round(2)
        print(decade_summary)
        
        return {
            'country_summary': country_summary,
            'source_summary': source_summary,
            'decade_summary': decade_summary
        }
    
    def save_merged_data(self, output_path="data/processed/comprehensive_merged_bond_yields.csv"):
        """Save the merged and cleaned dataset"""
        print(f"Saving comprehensive merged data to {output_path}...")
        
        if self.merged_data is None:
            print("No data to save!")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save the data
        self.merged_data.to_csv(output_path, index=False)
        print(f"Data saved successfully!")
        
        # Also save a summary file
        summary_path = output_path.replace('.csv', '_summary.txt')
        with open(summary_path, 'w') as f:
            f.write("COMPREHENSIVE BOND YIELD DATA MERGE SUMMARY\n")
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
    
    def run_full_pipeline(self):
        """Run the complete data merging and cleaning pipeline"""
        print("=" * 70)
        print("COMPREHENSIVE BOND YIELD DATA MERGING AND CLEANING PIPELINE")
        print("=" * 70)
        
        # Step 1: Load all data
        merged_data = self.load_all_yield_data()
        
        if merged_data is None:
            print("Pipeline failed: No data could be loaded")
            return None
        
        # Step 2: Clean data
        cleaned_data = self.clean_data()
        
        if cleaned_data is None:
            print("Pipeline failed: Data cleaning failed")
            return None
        
        # Step 3: Generate summary statistics
        summary_stats = self.generate_summary_stats()
        
        # Step 4: Save data
        self.save_merged_data()
        
        print("\n" + "=" * 70)
        print("COMPREHENSIVE PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        
        return self.merged_data

def main():
    """Main function to run the comprehensive bond data merging pipeline"""
    merger = ComprehensiveBondDataMerger()
    merged_data = merger.run_full_pipeline()
    
    if merged_data is not None:
        print(f"\nFinal dataset shape: {merged_data.shape}")
        print(f"Available countries: {sorted(merged_data['Country'].unique())}")
        print(f"Data sources: {sorted(merged_data['source'].unique())}")
    else:
        print("Pipeline failed!")

if __name__ == "__main__":
    main() 