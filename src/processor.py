import pandas as pd
import os

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        """Load and clean the CSV data."""
        print(f"[*] Loading data from {self.file_path}...")
        # Note: CSV has duplicate 'Ticker' column
        self.df = pd.read_csv(self.file_path)
        
        # Convert Date/Time to datetime object
        self.df['Date'] = pd.to_datetime(self.df['Date'], format='%d-%b-%y %H:%M:%S', errors='coerce')
        
        # Drop unnecessary duplicate Ticker column if exists (pandas usually names it Ticker.1)
        if 'Ticker.1' in self.df.columns:
            self.df = self.df.drop(columns=['Ticker.1'])
            
        print(f"[+] Loaded {len(self.df)} rows.")
        return self.df

    def filter_recent_week(self):
        """Filter data to only include the last 7 calendar days from the latest date."""
        if self.df is not None and not self.df.empty:
            latest_date = self.df['Date'].max()
            start_date = latest_date - pd.Timedelta(days=7)
            self.df = self.df[self.df['Date'] >= start_date]
        return self.df

    def get_date_range_str(self):
        """Get formatted date range string for titles."""
        if self.df is None or self.df.empty:
            return ""
        min_date = self.df['Date'].min().strftime('%d/%m/%Y')
        max_date = self.df['Date'].max().strftime('%d/%m/%Y')
        if min_date == max_date:
            return min_date
        return f"{min_date} - {max_date}"

    def get_market_summary(self):
        """Calculate daily net flow for Foreign and Proprietary investors."""
        summary = self.df.groupby('Date').agg({
            'GT NN Net': 'sum',
            'GT TD Net': 'sum'
        }).reset_index()
        
        # Sort by date
        summary = summary.sort_values('Date')
        return summary

    def get_top_tickers(self, n=10, group='NN'):
        """Get top N tickers by net value for a specific group (NN or TD)."""
        col = f'GT {group} Net'
        
        # Top Net Buy
        top_buy = self.df.groupby('Ticker')[col].sum().sort_values(ascending=False).head(n)
        
        # Top Net Sell
        top_sell = self.df.groupby('Ticker')[col].sum().sort_values(ascending=True).head(n)
        
        return top_buy, top_sell

if __name__ == "__main__":
    # Test logic
    data_path = os.path.join('data', 'NN_TD.csv')
    if os.path.exists(data_path):
        processor = DataProcessor(data_path)
        df = processor.load_data()
        print(processor.get_market_summary().tail())
