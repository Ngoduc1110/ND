import pandas as pd
from datetime import datetime, timedelta

class IndustryProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load and clean the industry CSV data."""
        print(f"[*] Loading industry data from {self.file_path}...")
        self.df = pd.read_csv(self.file_path, on_bad_lines='skip')
        
        # Date format in CHISONGANH is like '04-Jan-10 00:00:00'
        # Let's convert it to datetime
        self.df['Date/Time'] = pd.to_datetime(self.df['Date/Time'], errors='coerce')
        
        # Drop rows with invalid dates
        self.df = self.df.dropna(subset=['Date/Time'])
        
        # Sort by Date
        self.df = self.df.sort_values(by='Date/Time')
        print(f"[+] Loaded {len(self.df)} rows of industry data.")
        return self.df

    def get_recent_data(self, months=3):
        """Filter data for the last X months."""
        if self.df is None or self.df.empty:
            return pd.DataFrame()
            
        latest_date = self.df['Date/Time'].max()
        start_date = latest_date - pd.DateOffset(months=months)
        recent_df = self.df[self.df['Date/Time'] >= start_date].copy()
        return recent_df

    def get_top_industries(self, df, top_n=5):
        """Get the names of the top N industries by total volume in the given dataframe."""
        if df.empty:
            return []
            
        # Group by industry ('Ten Cty') and sum Volume
        volume_by_industry = df.groupby('Ten Cty')['Volume'].sum()
        top_industries = volume_by_industry.sort_values(ascending=False).head(top_n).index.tolist()
        return top_industries
