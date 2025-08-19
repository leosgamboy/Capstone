#!/usr/bin/env python3
"""
Bond Yield Data Analysis Script

This script performs comprehensive analysis of the merged bond yield data,
including descriptive statistics, time series analysis, and visualizations.

Features:
- Descriptive statistics by country and time period
- Time series plots and trends
- Correlation analysis between countries
- Volatility analysis
- Historical event analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class BondDataAnalyzer:
    def __init__(self, data_path="data/processed/merged_bond_yields.csv"):
        self.data_path = data_path
        self.df = None
        self.output_dir = "outputs/plots"
        
        # Create output directory
        import os
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_data(self):
        """Load the merged bond yield data"""
        print("Loading merged bond yield data...")
        self.df = pd.read_csv(self.data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        
        print(f"Loaded {len(self.df)} records")
        print(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        print(f"Countries: {sorted(self.df['Country'].unique())}")
        
        return self.df
    
    def basic_statistics(self):
        """Generate basic descriptive statistics"""
        print("\n=== BASIC STATISTICS ===")
        
        # Overall statistics
        print(f"Total observations: {len(self.df):,}")
        print(f"Date range: {self.df['Date'].min()} to {self.df['Date'].max()}")
        print(f"Countries: {self.df['Country'].nunique()}")
        
        # Statistics by country
        print("\nStatistics by Country:")
        country_stats = self.df.groupby('Country')['yield_rate'].agg([
            'count', 'mean', 'std', 'min', 'max', 'median'
        ]).round(3)
        print(country_stats)
        
        # Statistics by decade
        print("\nStatistics by Decade:")
        decade_stats = self.df.groupby('Decade')['yield_rate'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(3)
        print(decade_stats)
        
        return country_stats, decade_stats
    
    def plot_yield_trends(self):
        """Plot yield trends over time for each country"""
        print("Creating yield trend plots...")
        
        # Create figure with subplots
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle('10-Year Government Bond Yields Over Time', fontsize=16)
        
        countries = sorted(self.df['Country'].unique())
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, (country, color) in enumerate(zip(countries, colors)):
            country_data = self.df[self.df['Country'] == country].copy()
            country_data = country_data.sort_values('Date')
            
            # Plot the data
            axes[i].plot(country_data['Date'], country_data['yield_rate'], 
                        color=color, linewidth=1, alpha=0.8)
            
            # Add rolling average
            rolling_avg = country_data['yield_rate'].rolling(window=252).mean()
            axes[i].plot(country_data['Date'], rolling_avg, 
                        color='red', linewidth=2, alpha=0.7, label='12-Month Rolling Average')
            
            axes[i].set_title(f'{country} 10-Year Bond Yields', fontsize=12)
            axes[i].set_ylabel('Yield Rate (%)')
            axes[i].grid(True, alpha=0.3)
            axes[i].legend()
            
            # Add some key historical periods
            if country == 'United States':
                # Add some key periods
                axes[i].axvspan(pd.Timestamp('2008-01-01'), pd.Timestamp('2009-12-31'), 
                               alpha=0.2, color='red', label='Financial Crisis')
                axes[i].axvspan(pd.Timestamp('2020-01-01'), pd.Timestamp('2021-12-31'), 
                               alpha=0.2, color='orange', label='COVID-19')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/yield_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_yield_distribution(self):
        """Plot yield distribution by country"""
        print("Creating yield distribution plots...")
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Distribution of 10-Year Bond Yields by Country', fontsize=16)
        
        countries = sorted(self.df['Country'].unique())
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, (country, color) in enumerate(zip(countries, colors)):
            country_data = self.df[self.df['Country'] == country]['yield_rate']
            
            # Histogram
            axes[i].hist(country_data, bins=50, alpha=0.7, color=color, edgecolor='black')
            axes[i].axvline(country_data.mean(), color='red', linestyle='--', 
                           linewidth=2, label=f'Mean: {country_data.mean():.2f}%')
            axes[i].axvline(country_data.median(), color='green', linestyle='--', 
                           linewidth=2, label=f'Median: {country_data.median():.2f}%')
            
            axes[i].set_title(f'{country} Yield Distribution', fontsize=12)
            axes[i].set_xlabel('Yield Rate (%)')
            axes[i].set_ylabel('Frequency')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/yield_distributions.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_correlation_heatmap(self):
        """Plot correlation heatmap between countries"""
        print("Creating correlation heatmap...")
        
        # Pivot data to get countries as columns
        pivot_df = self.df.pivot(index='Date', columns='Country', values='yield_rate')
        
        # Calculate correlation matrix
        corr_matrix = pivot_df.corr()
        
        # Create heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5)
        plt.title('Correlation Matrix: 10-Year Bond Yields', fontsize=16)
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return corr_matrix
    
    def plot_volatility_analysis(self):
        """Analyze and plot yield volatility over time"""
        print("Creating volatility analysis plots...")
        
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle('Yield Volatility Analysis (12-Month Rolling Standard Deviation)', fontsize=16)
        
        countries = sorted(self.df['Country'].unique())
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        for i, (country, color) in enumerate(zip(countries, colors)):
            country_data = self.df[self.df['Country'] == country].copy()
            country_data = country_data.sort_values('Date')
            
            # Calculate rolling volatility (12-month window)
            rolling_vol = country_data['yield_rate'].rolling(window=252).std()
            
            axes[i].plot(country_data['Date'], rolling_vol, 
                        color=color, linewidth=2, alpha=0.8)
            axes[i].set_title(f'{country} Yield Volatility', fontsize=12)
            axes[i].set_ylabel('Volatility (Std Dev)')
            axes[i].grid(True, alpha=0.3)
            
            # Add mean volatility line
            mean_vol = rolling_vol.mean()
            axes[i].axhline(mean_vol, color='red', linestyle='--', 
                           alpha=0.7, label=f'Mean Volatility: {mean_vol:.3f}')
            axes[i].legend()
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/volatility_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def plot_recent_period_analysis(self):
        """Focus on recent period (last 20 years)"""
        print("Creating recent period analysis...")
        
        # Filter for last 20 years
        recent_data = self.df[self.df['Date'] >= '2005-01-01'].copy()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Recent Period Analysis (2005-2025)', fontsize=16)
        
        # Plot 1: Recent trends
        for country in sorted(recent_data['Country'].unique()):
            country_data = recent_data[recent_data['Country'] == country]
            axes[0, 0].plot(country_data['Date'], country_data['yield_rate'], 
                           label=country, linewidth=2)
        
        axes[0, 0].set_title('Recent Yield Trends')
        axes[0, 0].set_ylabel('Yield Rate (%)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Box plot by country
        recent_data.boxplot(column='yield_rate', by='Country', ax=axes[0, 1])
        axes[0, 1].set_title('Yield Distribution by Country')
        axes[0, 1].set_ylabel('Yield Rate (%)')
        
        # Plot 3: Monthly averages
        monthly_data = recent_data.groupby([recent_data['Date'].dt.to_period('M'), 'Country'])['yield_rate'].mean().reset_index()
        monthly_data['Date'] = monthly_data['Date'].astype(str).apply(pd.to_datetime)
        
        for country in sorted(monthly_data['Country'].unique()):
            country_data = monthly_data[monthly_data['Country'] == country]
            axes[1, 0].plot(country_data['Date'], country_data['yield_rate'], 
                           label=country, linewidth=2)
        
        axes[1, 0].set_title('Monthly Average Yields')
        axes[1, 0].set_ylabel('Yield Rate (%)')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Correlation in recent period
        recent_pivot = recent_data.pivot(index='Date', columns='Country', values='yield_rate')
        recent_corr = recent_pivot.corr()
        
        sns.heatmap(recent_corr, annot=True, cmap='coolwarm', center=0, 
                   square=True, linewidths=0.5, ax=axes[1, 1])
        axes[1, 1].set_title('Recent Period Correlation')
        
        plt.tight_layout()
        plt.savefig(f'{self.output_dir}/recent_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        print("Generating summary report...")
        
        report = []
        report.append("BOND YIELD DATA ANALYSIS REPORT")
        report.append("=" * 50)
        report.append(f"Generated on: {datetime.now()}")
        report.append(f"Data period: {self.df['Date'].min()} to {self.df['Date'].max()}")
        report.append(f"Total observations: {len(self.df):,}")
        report.append("")
        
        # Country summary
        report.append("COUNTRY SUMMARY:")
        report.append("-" * 20)
        country_stats = self.df.groupby('Country')['yield_rate'].agg([
            'count', 'mean', 'std', 'min', 'max', 'median'
        ]).round(3)
        report.append(str(country_stats))
        report.append("")
        
        # Recent period summary (last 10 years)
        recent_data = self.df[self.df['Date'] >= '2015-01-01']
        report.append("RECENT PERIOD SUMMARY (2015-2025):")
        report.append("-" * 40)
        recent_stats = recent_data.groupby('Country')['yield_rate'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(3)
        report.append(str(recent_stats))
        report.append("")
        
        # Key insights
        report.append("KEY INSIGHTS:")
        report.append("-" * 15)
        
        # Highest and lowest yields
        max_yield = self.df.loc[self.df['yield_rate'].idxmax()]
        min_yield = self.df.loc[self.df['yield_rate'].idxmin()]
        
        report.append(f"Highest yield: {max_yield['yield_rate']:.2f}% ({max_yield['Country']}, {max_yield['Date'].strftime('%Y-%m-%d')})")
        report.append(f"Lowest yield: {min_yield['yield_rate']:.2f}% ({min_yield['Country']}, {min_yield['Date'].strftime('%Y-%m-%d')})")
        
        # Most volatile country
        volatility_by_country = self.df.groupby('Country')['yield_rate'].std().sort_values(ascending=False)
        most_volatile = volatility_by_country.index[0]
        report.append(f"Most volatile country: {most_volatile} (std dev: {volatility_by_country.iloc[0]:.3f})")
        
        # Save report
        report_path = f"{self.output_dir}/analysis_report.txt"
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
        
        print(f"Report saved to {report_path}")
        return '\n'.join(report)
    
    def run_full_analysis(self):
        """Run the complete analysis pipeline"""
        print("=" * 60)
        print("BOND YIELD DATA ANALYSIS PIPELINE")
        print("=" * 60)
        
        # Load data
        self.load_data()
        
        # Run analyses
        print("\n1. Basic Statistics")
        country_stats, decade_stats = self.basic_statistics()
        
        print("\n2. Yield Trends Analysis")
        self.plot_yield_trends()
        
        print("\n3. Yield Distribution Analysis")
        self.plot_yield_distribution()
        
        print("\n4. Correlation Analysis")
        corr_matrix = self.plot_correlation_heatmap()
        
        print("\n5. Volatility Analysis")
        self.plot_volatility_analysis()
        
        print("\n6. Recent Period Analysis")
        self.plot_recent_period_analysis()
        
        print("\n7. Generating Summary Report")
        report = self.generate_summary_report()
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print(f"\nOutput files saved to: {self.output_dir}/")
        print("Generated files:")
        print("- yield_trends.png")
        print("- yield_distributions.png") 
        print("- correlation_heatmap.png")
        print("- volatility_analysis.png")
        print("- recent_analysis.png")
        print("- analysis_report.txt")
        
        return {
            'country_stats': country_stats,
            'decade_stats': decade_stats,
            'correlation_matrix': corr_matrix,
            'report': report
        }

def main():
    """Main function to run the bond data analysis"""
    analyzer = BondDataAnalyzer()
    results = analyzer.run_full_analysis()
    
    print(f"\nAnalysis completed! Check the outputs/plots/ directory for visualizations.")

if __name__ == "__main__":
    main() 