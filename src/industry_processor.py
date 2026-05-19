import pandas as pd
from datetime import datetime, timedelta

class IndustryProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load and clean the industry CSV data handling extra commas in Ten Cty."""
        print(f"[*] Loading industry data from {self.file_path}...")
        
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        header = [c.strip() for c in lines[0].strip().split(',')]
        data = []
        for line in lines[1:]:
            parts = [p.strip() for p in line.strip().split(',')]
            if not parts or parts == ['']:
                continue
            if len(parts) > 9:
                ticker = parts[0]
                date_time = parts[1]
                numeric_fields = parts[-6:]
                company_name = ",".join(parts[2:-6])
                data.append([ticker, date_time, company_name] + numeric_fields)
            else:
                data.append(parts)
                
        self.df = pd.DataFrame(data, columns=header)
        
        # Convert numeric columns
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'Open Interest']
        for col in numeric_cols:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            
        # Date format in CHISONGANH is like '04-Jan-10 00:00:00'
        self.df['Date/Time'] = pd.to_datetime(self.df['Date/Time'], format='%d-%b-%y %H:%M:%S', errors='coerce')
        
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
