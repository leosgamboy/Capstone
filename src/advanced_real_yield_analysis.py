#!/usr/bin/env python3
"""
Advanced Real Yield Data Analysis Script

This script performs comprehensive analysis of the real bond yield data:
- Advanced visualizations with real historical trends
- Time series analysis on actual market movements
- Forecasting models using real yield patterns
- Correlation analysis between real country yields
- Historical events impact analysis

Features:
- Real historical data spanning 348 years (1677-2025)
- 73 countries with actual market data
- Advanced statistical analysis and visualizations
- Time series forecasting models
- Correlation and cointegration analysis
- Historical event impact studies
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
import os
warnings.filterwarnings('ignore')

# Advanced libraries for time series analysis
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller, coint
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class AdvancedRealYieldAnalyzer:
    def __init__(self, data_path="data/processed/real_merged_bond_yields.csv"):
        self.data_path = data_path
        self.data = None
        self.major_countries = [
            'United States', 'Germany', 'Japan', 'United Kingdom', 
            'France', 'Italy', 'Canada', 'Australia', 'Switzerland',
            'Netherlands', 'Spain', 'Sweden', 'Norway', 'Denmark'
        ]
        
        # Historical events for analysis
        self.historical_events = {
            '2008 Financial Crisis': ('2008-09-01', '2009-03-31'),
            '2010 Euro Crisis': ('2010-01-01', '2012-12-31'),
            'COVID-19 Pandemic': ('2020-03-01', '2021-12-31'),
            'Great Depression': ('1929-10-01', '1939-12-31'),
            'World War II': ('1939-09-01', '1945-09-01'),
            'Oil Crisis 1973': ('1973-10-01', '1975-12-31'),
            'Dot-com Bubble': ('2000-03-01', '2002-12-31'),
            'Global Financial Crisis': ('2007-08-01', '2009-12-31')
        }
    
    def load_real_data(self):
        """Load the real yield data"""
        print("Loading real yield data...")
        self.data = pd.read_csv(self.data_path)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        
        # Filter to reasonable date range (1800 onwards) to avoid timestamp issues
        self.data = self.data[self.data['Date'] >= '1800-01-01']
        
        print(f"Loaded {len(self.data):,} records (filtered from 1800 onwards)")
        print(f"Date range: {self.data['Date'].min()} to {self.data['Date'].max()}")
        print(f"Countries: {self.data['Country'].nunique()}")
        
        return self.data
    
    def create_advanced_visualizations(self):
        """Create advanced visualizations with real historical trends"""
        print("\n📊 Creating advanced visualizations...")
        
        # 1. Long-term historical trends for major countries
        self.plot_long_term_trends()
        
        # 2. Yield distribution analysis
        self.plot_yield_distributions()
        
        # 3. Volatility analysis
        self.plot_volatility_analysis()
        
        # 4. Regional comparison
        self.plot_regional_comparison()
        
        # 5. Interactive time series
        self.create_interactive_timeline()
    
    def plot_long_term_trends(self):
        """Plot long-term historical trends for major countries"""
        fig, axes = plt.subplots(2, 2, figsize=(20, 12))
        fig.suptitle('Long-term Historical Bond Yield Trends (Real Data)', fontsize=16, fontweight='bold')
        
        # Filter for major countries with long histories
        major_data = self.data[self.data['Country'].isin(self.major_countries)]
        
        # Plot 1: Very long-term trends (1700-2025)
        ax1 = axes[0, 0]
        long_history_countries = ['United Kingdom', 'France', 'Netherlands', 'Germany']
        for country in long_history_countries:
            country_data = major_data[major_data['Country'] == country]
            if len(country_data) > 0:
                # Resample to annual data for clarity
                annual_data = country_data.set_index('Date')['yield_rate'].resample('Y').mean()
                ax1.plot(annual_data.index, annual_data.values, label=country, linewidth=2, alpha=0.8)
        
        ax1.set_title('Very Long-term Trends (1700-2025)')
        ax1.set_ylabel('Yield Rate (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Modern era trends (1900-2025)
        ax2 = axes[0, 1]
        modern_countries = ['United States', 'United Kingdom', 'Germany', 'Japan']
        for country in modern_countries:
            country_data = major_data[major_data['Country'] == country]
            if len(country_data) > 0:
                # Resample to monthly data
                monthly_data = country_data.set_index('Date')['yield_rate'].resample('M').mean()
                ax2.plot(monthly_data.index, monthly_data.values, label=country, linewidth=2, alpha=0.8)
        
        ax2.set_title('Modern Era Trends (1900-2025)')
        ax2.set_ylabel('Yield Rate (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Recent trends (2000-2025)
        ax3 = axes[1, 0]
        recent_data = major_data[major_data['Date'] >= '2000-01-01']
        for country in self.major_countries[:8]:
            country_data = recent_data[recent_data['Country'] == country]
            if len(country_data) > 0:
                ax3.plot(country_data['Date'], country_data['yield_rate'], label=country, linewidth=1.5, alpha=0.8)
        
        ax3.set_title('Recent Trends (2000-2025)')
        ax3.set_ylabel('Yield Rate (%)')
        ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Crisis periods comparison
        ax4 = axes[1, 1]
        crisis_periods = {
            '2008 Crisis': ('2008-01-01', '2009-12-31'),
            'COVID-19': ('2020-01-01', '2021-12-31'),
            'Euro Crisis': ('2010-01-01', '2012-12-31')
        }
        
        colors = ['red', 'orange', 'purple']
        for i, (crisis, (start, end)) in enumerate(crisis_periods.items()):
            crisis_data = major_data[
                (major_data['Date'] >= start) & 
                (major_data['Date'] <= end) &
                (major_data['Country'] == 'United States')
            ]
            if len(crisis_data) > 0:
                ax4.plot(crisis_data['Date'], crisis_data['yield_rate'], 
                        label=crisis, color=colors[i], linewidth=2)
        
        ax4.set_title('Crisis Periods Comparison (US Yields)')
        ax4.set_ylabel('Yield Rate (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/plots/advanced_long_term_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_yield_distributions(self):
        """Plot yield distribution analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Yield Distribution Analysis (Real Data)', fontsize=16, fontweight='bold')
        
        # Plot 1: Global yield distribution
        ax1 = axes[0, 0]
        ax1.hist(self.data['yield_rate'], bins=100, alpha=0.7, edgecolor='black', density=True)
        ax1.set_title('Global Yield Distribution')
        ax1.set_xlabel('Yield Rate (%)')
        ax1.set_ylabel('Density')
        ax1.axvline(self.data['yield_rate'].mean(), color='red', linestyle='--', 
                    label=f'Mean: {self.data["yield_rate"].mean():.2f}%')
        ax1.legend()
        
        # Plot 2: Yield distribution by region
        ax2 = axes[0, 1]
        regions = self.data['Region'].unique()
        for region in regions:
            region_data = self.data[self.data['Region'] == region]['yield_rate']
            ax2.hist(region_data, bins=50, alpha=0.5, label=region, density=True)
        ax2.set_title('Yield Distribution by Region')
        ax2.set_xlabel('Yield Rate (%)')
        ax2.set_ylabel('Density')
        ax2.legend()
        
        # Plot 3: Box plot by major countries
        ax3 = axes[1, 0]
        major_data = self.data[self.data['Country'].isin(self.major_countries[:10])]
        sns.boxplot(data=major_data, x='Country', y='yield_rate', ax=ax3)
        ax3.set_title('Yield Distribution by Major Countries')
        ax3.set_ylabel('Yield Rate (%)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Plot 4: Yield percentiles over time
        ax4 = axes[1, 1]
        # Calculate percentiles by year
        yearly_percentiles = self.data.groupby(self.data['Date'].dt.year)['yield_rate'].agg([
            'mean', 'std', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)
        ]).rename(columns={'<lambda_0>': 'Q25', '<lambda_1>': 'Q75'})
        
        ax4.fill_between(yearly_percentiles.index, 
                        yearly_percentiles['Q25'], 
                        yearly_percentiles['Q75'], 
                        alpha=0.3, label='25th-75th Percentile')
        ax4.plot(yearly_percentiles.index, yearly_percentiles['mean'], 
                linewidth=2, label='Mean', color='red')
        ax4.set_title('Global Yield Percentiles Over Time')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Yield Rate (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('outputs/plots/advanced_yield_distributions.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_volatility_analysis(self):
        """Plot volatility analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Volatility Analysis (Real Data)', fontsize=16, fontweight='bold')
        
        # Calculate rolling volatility for major countries
        major_data = self.data[self.data['Country'].isin(self.major_countries[:8])]
        
        # Plot 1: Rolling volatility comparison
        ax1 = axes[0, 0]
        for country in self.major_countries[:8]:
            country_data = major_data[major_data['Country'] == country]
            if len(country_data) > 0:
                # Calculate 30-day rolling volatility
                country_data = country_data.sort_values('Date').set_index('Date')
                rolling_vol = country_data['yield_rate'].rolling(window=30).std()
                ax1.plot(rolling_vol.index, rolling_vol.values, label=country, alpha=0.8)
        
        ax1.set_title('30-Day Rolling Volatility')
        ax1.set_ylabel('Volatility (Standard Deviation)')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Volatility by decade
        ax2 = axes[0, 1]
        decade_vol = self.data.groupby(self.data['Date'].dt.year // 10 * 10)['yield_rate'].std()
        ax2.bar(decade_vol.index, decade_vol.values, alpha=0.7)
        ax2.set_title('Yield Volatility by Decade')
        ax2.set_xlabel('Decade')
        ax2.set_ylabel('Standard Deviation')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Volatility heatmap by country and year
        ax3 = axes[1, 0]
        vol_data = self.data.groupby(['Country', self.data['Date'].dt.year])['yield_rate'].std().reset_index()
        vol_pivot = vol_data.pivot(index='Country', columns='Date', values='yield_rate')
        
        # Select countries with most data
        top_countries = vol_pivot.count(axis=1).nlargest(15).index
        vol_pivot_filtered = vol_pivot.loc[top_countries]
        
        sns.heatmap(vol_pivot_filtered, ax=ax3, cmap='YlOrRd', cbar_kws={'label': 'Volatility'})
        ax3.set_title('Volatility Heatmap by Country and Year')
        
        # Plot 4: Crisis period volatility
        ax4 = axes[1, 1]
        crisis_data = self.data[
            (self.data['Date'] >= '2007-01-01') & 
            (self.data['Date'] <= '2012-12-31')
        ]
        
        crisis_vol = crisis_data.groupby('Country')['yield_rate'].std().sort_values(ascending=False).head(15)
        crisis_vol.plot(kind='bar', ax=ax4)
        ax4.set_title('Volatility During Financial Crisis (2007-2012)')
        ax4.set_ylabel('Standard Deviation')
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('outputs/plots/advanced_volatility_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_regional_comparison(self):
        """Plot regional comparison analysis"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Regional Comparison Analysis (Real Data)', fontsize=16, fontweight='bold')
        
        # Plot 1: Regional average yields over time
        ax1 = axes[0, 0]
        regional_ts = self.data.groupby(['Date', 'Region'])['yield_rate'].mean().reset_index()
        for region in regional_ts['Region'].unique():
            region_data = regional_ts[regional_ts['Region'] == region]
            ax1.plot(region_data['Date'], region_data['yield_rate'], label=region, alpha=0.8)
        
        ax1.set_title('Regional Average Yields Over Time')
        ax1.set_ylabel('Yield Rate (%)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Regional yield spreads
        ax2 = axes[0, 1]
        # Calculate spread relative to US yields
        us_yields = self.data[self.data['Country'] == 'United States'].set_index('Date')['yield_rate']
        regional_spreads = {}
        
        for region in self.data['Region'].unique():
            region_data = self.data[self.data['Region'] == region]
            if len(region_data) > 0:
                region_avg = region_data.groupby('Date')['yield_rate'].mean()
                # Align with US data
                aligned_data = pd.concat([region_avg, us_yields], axis=1).dropna()
                if len(aligned_data) > 0:
                    spread = aligned_data.iloc[:, 0] - aligned_data.iloc[:, 1]
                    regional_spreads[region] = spread
        
        for region, spread in regional_spreads.items():
            ax2.plot(spread.index, spread.values, label=region, alpha=0.8)
        
        ax2.set_title('Regional Yield Spreads vs US')
        ax2.set_ylabel('Spread (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Regional correlation matrix
        ax3 = axes[1, 0]
        regional_corr = regional_ts.pivot(index='Date', columns='Region', values='yield_rate').corr()
        sns.heatmap(regional_corr, annot=True, cmap='coolwarm', center=0, ax=ax3)
        ax3.set_title('Regional Yield Correlations')
        
        # Plot 4: Regional volatility comparison
        ax4 = axes[1, 1]
        regional_vol = self.data.groupby('Region')['yield_rate'].agg(['mean', 'std']).round(2)
        regional_vol.plot(kind='bar', ax=ax4)
        ax4.set_title('Regional Yield Statistics')
        ax4.set_ylabel('Yield Rate (%)')
        ax4.legend(['Mean', 'Std Dev'])
        ax4.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('outputs/plots/advanced_regional_comparison.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def create_interactive_timeline(self):
        """Create interactive timeline visualization"""
        print("Creating interactive timeline...")
        
        # Prepare data for interactive plot
        timeline_data = self.data.groupby(['Date', 'Country'])['yield_rate'].mean().reset_index()
        
        # Create interactive plot
        fig = px.line(timeline_data, x='Date', y='yield_rate', color='Country',
                     title='Interactive Bond Yield Timeline (Real Data)',
                     labels={'yield_rate': 'Yield Rate (%)', 'Date': 'Date'},
                     hover_data=['Country', 'yield_rate'])
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Yield Rate (%)",
            hovermode='x unified'
        )
        
        # Save as HTML for interactive viewing
        fig.write_html('outputs/plots/interactive_yield_timeline.html')
        print("Interactive timeline saved to outputs/plots/interactive_yield_timeline.html")
    
    def perform_time_series_analysis(self):
        """Perform time series analysis on actual market movements"""
        print("\n📈 Performing time series analysis...")
        
        # Focus on major countries with long histories
        analysis_countries = ['United States', 'Germany', 'United Kingdom', 'Japan']
        
        for country in analysis_countries:
            print(f"\n--- {country} Time Series Analysis ---")
            country_data = self.data[self.data['Country'] == country].sort_values('Date')
            
            if len(country_data) > 0:
                # Prepare time series
                ts_data = country_data.set_index('Date')['yield_rate'].resample('M').mean()
                
                # 1. Stationarity test
                adf_result = adfuller(ts_data.dropna())
                print(f"ADF Test p-value: {adf_result[1]:.4f}")
                print(f"Stationary: {adf_result[1] < 0.05}")
                
                # 2. Decomposition
                if len(ts_data) > 12:
                    decomposition = seasonal_decompose(ts_data.dropna(), period=12)
                    
                    # Plot decomposition
                    fig, axes = plt.subplots(4, 1, figsize=(12, 10))
                    fig.suptitle(f'{country} Yield Decomposition', fontsize=14)
                    
                    decomposition.observed.plot(ax=axes[0], title='Observed')
                    decomposition.trend.plot(ax=axes[1], title='Trend')
                    decomposition.seasonal.plot(ax=axes[2], title='Seasonal')
                    decomposition.resid.plot(ax=axes[3], title='Residual')
                    
                    plt.tight_layout()
                    plt.savefig(f'outputs/plots/{country.replace(" ", "_")}_decomposition.png', dpi=300, bbox_inches='tight')
                    plt.show()
                
                # 3. Basic statistics
                print(f"Mean: {ts_data.mean():.2f}%")
                print(f"Std Dev: {ts_data.std():.2f}%")
                print(f"Min: {ts_data.min():.2f}%")
                print(f"Max: {ts_data.max():.2f}%")
    
    def build_forecasting_models(self):
        """Build forecasting models using real yield patterns"""
        print("\n🔮 Building forecasting models...")
        
        # Focus on US yields for forecasting (most complete data)
        us_data = self.data[self.data['Country'] == 'United States'].sort_values('Date')
        
        if len(us_data) > 0:
            # Prepare data
            ts_data = us_data.set_index('Date')['yield_rate'].resample('M').mean()
            
            # Split data for forecasting
            train_size = int(len(ts_data) * 0.8)
            train_data = ts_data[:train_size]
            test_data = ts_data[train_size:]
            
            print(f"Training on {len(train_data)} months, testing on {len(test_data)} months")
            
            # ARIMA model
            try:
                model = ARIMA(train_data.dropna(), order=(1, 1, 1))
                fitted_model = model.fit()
                
                # Forecast
                forecast = fitted_model.forecast(steps=len(test_data))
                
                # Calculate metrics
                mse = mean_squared_error(test_data.dropna(), forecast[:len(test_data.dropna())])
                mae = mean_absolute_error(test_data.dropna(), forecast[:len(test_data.dropna())])
                
                print(f"ARIMA(1,1,1) Model:")
                print(f"MSE: {mse:.4f}")
                print(f"MAE: {mae:.4f}")
                
                # Plot forecast
                plt.figure(figsize=(12, 6))
                plt.plot(train_data.index, train_data.values, label='Training Data', alpha=0.7)
                plt.plot(test_data.index, test_data.values, label='Actual Test Data', alpha=0.7)
                plt.plot(test_data.index, forecast, label='Forecast', linestyle='--', alpha=0.8)
                plt.title('US 10-Year Yield Forecast (ARIMA Model)')
                plt.xlabel('Date')
                plt.ylabel('Yield Rate (%)')
                plt.legend()
                plt.grid(True, alpha=0.3)
                plt.savefig('outputs/plots/us_yield_forecast.png', dpi=300, bbox_inches='tight')
                plt.show()
                
            except Exception as e:
                print(f"Forecasting error: {e}")
    
    def analyze_correlations(self):
        """Analyze correlations between real country yields"""
        print("\n🔗 Analyzing correlations between country yields...")
        
        # Create pivot table for correlation analysis
        pivot_data = self.data.pivot_table(
            index='Date', columns='Country', values='yield_rate', aggfunc='mean'
        )
        
        # Focus on major countries with sufficient data
        major_countries_data = pivot_data[self.major_countries].dropna()
        
        if len(major_countries_data) > 0:
            # 1. Correlation matrix
            correlation_matrix = major_countries_data.corr()
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
                       square=True, fmt='.2f')
            plt.title('Country Yield Correlations (Real Data)')
            plt.tight_layout()
            plt.savefig('outputs/plots/country_correlations.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            # 2. Cointegration analysis
            print("\n--- Cointegration Analysis ---")
            for i, country1 in enumerate(major_countries_data.columns[:5]):
                for country2 in major_countries_data.columns[i+1:6]:
                    try:
                        score, pvalue, _ = coint(major_countries_data[country1].dropna(), 
                                                major_countries_data[country2].dropna())
                        print(f"{country1} vs {country2}: p-value = {pvalue:.4f}")
                    except:
                        continue
            
            # 3. Rolling correlations
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Rolling Correlations (Real Data)', fontsize=16)
            
            # US vs major countries
            us_data = major_countries_data['United States']
            for i, country in enumerate(['Germany', 'United Kingdom', 'Japan', 'France']):
                if country in major_countries_data.columns:
                    country_data = major_countries_data[country]
                    # Calculate 60-day rolling correlation
                    rolling_corr = us_data.rolling(60).corr(country_data)
                    
                    ax = axes[i//2, i%2]
                    ax.plot(rolling_corr.index, rolling_corr.values, alpha=0.8)
                    ax.set_title(f'US vs {country} (60-day rolling)')
                    ax.set_ylabel('Correlation')
                    ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('outputs/plots/rolling_correlations.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def study_historical_events(self):
        """Study historical events and their impact on yields"""
        print("\n📚 Studying historical events impact...")
        
        # Focus on US yields for historical analysis
        us_data = self.data[self.data['Country'] == 'United States'].sort_values('Date')
        
        if len(us_data) > 0:
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('Historical Events Impact on Yields (Real Data)', fontsize=16)
            
            # Plot 1: Major crisis periods
            ax1 = axes[0, 0]
            for event, (start, end) in list(self.historical_events.items())[:4]:
                event_data = us_data[
                    (us_data['Date'] >= start) & 
                    (us_data['Date'] <= end)
                ]
                if len(event_data) > 0:
                    ax1.plot(event_data['Date'], event_data['yield_rate'], 
                            label=event, linewidth=2, alpha=0.8)
            
            ax1.set_title('Major Crisis Periods')
            ax1.set_ylabel('US 10-Year Yield (%)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Plot 2: Pre and post crisis comparison
            ax2 = axes[0, 1]
            crisis_comparison = {}
            for event, (start, end) in list(self.historical_events.items())[:4]:
                # Get data 1 year before and after crisis
                start_date = pd.to_datetime(start) - timedelta(days=365)
                end_date = pd.to_datetime(end) + timedelta(days=365)
                
                event_data = us_data[
                    (us_data['Date'] >= start_date) & 
                    (us_data['Date'] <= end_date)
                ]
                if len(event_data) > 0:
                    crisis_comparison[event] = event_data
            
            for event, data in crisis_comparison.items():
                ax2.plot(data['Date'], data['yield_rate'], label=event, alpha=0.8)
            
            ax2.set_title('Crisis Periods with Context')
            ax2.set_ylabel('US 10-Year Yield (%)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Plot 3: Yield changes during events
            ax3 = axes[1, 0]
            event_changes = {}
            for event, (start, end) in self.historical_events.items():
                event_data = us_data[
                    (us_data['Date'] >= start) & 
                    (us_data['Date'] <= end)
                ]
                if len(event_data) > 0:
                    change = event_data['yield_rate'].iloc[-1] - event_data['yield_rate'].iloc[0]
                    event_changes[event] = change
            
            events = list(event_changes.keys())
            changes = list(event_changes.values())
            colors = ['red' if x > 0 else 'blue' for x in changes]
            
            ax3.bar(events, changes, color=colors, alpha=0.7)
            ax3.set_title('Yield Changes During Historical Events')
            ax3.set_ylabel('Yield Change (%)')
            ax3.tick_params(axis='x', rotation=45)
            ax3.grid(True, alpha=0.3)
            
            # Plot 4: Volatility during events
            ax4 = axes[1, 1]
            event_volatility = {}
            for event, (start, end) in self.historical_events.items():
                event_data = us_data[
                    (us_data['Date'] >= start) & 
                    (us_data['Date'] <= end)
                ]
                if len(event_data) > 0:
                    volatility = event_data['yield_rate'].std()
                    event_volatility[event] = volatility
            
            events = list(event_volatility.keys())
            volatilities = list(event_volatility.values())
            
            ax4.bar(events, volatilities, alpha=0.7)
            ax4.set_title('Volatility During Historical Events')
            ax4.set_ylabel('Standard Deviation')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('outputs/plots/historical_events_impact.png', dpi=300, bbox_inches='tight')
            plt.show()
    
    def generate_comprehensive_report(self):
        """Generate a comprehensive analysis report"""
        print("\n📋 Generating comprehensive analysis report...")
        
        report_path = "outputs/results/advanced_real_yield_analysis_report.txt"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write("ADVANCED REAL YIELD DATA ANALYSIS REPORT\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated on: {datetime.now()}\n\n")
            
            f.write("DATASET OVERVIEW:\n")
            f.write("-" * 20 + "\n")
            f.write(f"Total records: {len(self.data):,}\n")
            f.write(f"Date range: {self.data['Date'].min()} to {self.data['Date'].max()}\n")
            f.write(f"Countries: {self.data['Country'].nunique()}\n")
            f.write(f"Time span: {self.data['Date'].max().year - self.data['Date'].min().year} years\n\n")
            
            f.write("KEY FINDINGS:\n")
            f.write("-" * 15 + "\n")
            
            # Global statistics
            global_mean = self.data['yield_rate'].mean()
            global_std = self.data['yield_rate'].std()
            f.write(f"• Global average yield: {global_mean:.2f}%\n")
            f.write(f"• Global yield volatility: {global_std:.2f}%\n")
            
            # Regional analysis
            regional_stats = self.data.groupby('Region')['yield_rate'].agg(['mean', 'std']).round(2)
            f.write(f"• Highest yielding region: {regional_stats['mean'].idxmax()} ({regional_stats['mean'].max():.2f}%)\n")
            f.write(f"• Lowest yielding region: {regional_stats['mean'].idxmin()} ({regional_stats['mean'].min():.2f}%)\n")
            
            # Historical insights
            f.write(f"• Oldest data: {self.data['Date'].min().year} ({self.data['Date'].min().year} years ago)\n")
            f.write(f"• Most comprehensive country: {self.data.groupby('Country').size().idxmax()}\n")
            
            f.write("\nANALYSIS COMPLETED:\n")
            f.write("-" * 20 + "\n")
            f.write("✅ Advanced visualizations with real historical trends\n")
            f.write("✅ Time series analysis on actual market movements\n")
            f.write("✅ Forecasting models using real yield patterns\n")
            f.write("✅ Correlation analysis between real country yields\n")
            f.write("✅ Historical events impact studies\n")
        
        print(f"📄 Comprehensive report saved to: {report_path}")
    
    def run_complete_analysis(self):
        """Run the complete advanced analysis pipeline"""
        print("🚀 Starting Advanced Real Yield Data Analysis...")
        
        # Step 1: Load real data
        self.load_real_data()
        
        # Step 2: Create advanced visualizations
        self.create_advanced_visualizations()
        
        # Step 3: Perform time series analysis
        self.perform_time_series_analysis()
        
        # Step 4: Build forecasting models
        self.build_forecasting_models()
        
        # Step 5: Analyze correlations
        self.analyze_correlations()
        
        # Step 6: Study historical events
        self.study_historical_events()
        
        # Step 7: Generate comprehensive report
        self.generate_comprehensive_report()
        
        print("\n" + "="*80)
        print("✅ ADVANCED REAL YIELD DATA ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*80)
        
        return self.data

def main():
    """Main function to run the advanced real yield analysis"""
    analyzer = AdvancedRealYieldAnalyzer()
    data = analyzer.run_complete_analysis()
    
    if data is not None:
        print(f"\n📈 Final Analysis Summary:")
        print(f"   Real dataset shape: {data.shape}")
        print(f"   Countries analyzed: {data['Country'].nunique()}")
        print(f"   Historical span: {data['Date'].max().year - data['Date'].min().year} years")
        print(f"\n📁 Advanced analysis outputs created in:")
        print(f"   • outputs/plots/ (advanced visualizations)")
        print(f"   • outputs/results/ (comprehensive report)")
        print(f"   • Interactive HTML timeline")
    else:
        print("❌ Advanced analysis failed!")

if __name__ == "__main__":
    main() 