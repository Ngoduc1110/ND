import pandas as pd
import os

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.full_df = None

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
        self.full_df = self.df.copy()
        return self.df

    def reset_filter(self):
        """Reset the current dataframe to the full loaded dataset."""
        if self.full_df is not None:
            self.df = self.full_df.copy()
        return self.df

    def filter_recent_week(self):
        """Filter data to only include the current business week (Monday to today)."""
        if self.full_df is not None and not self.full_df.empty:
            today = pd.Timestamp.now().normalize()
            # Find Monday of the current week (dayofweek: 0=Mon, 6=Sun)
            monday = today - pd.Timedelta(days=today.dayofweek)
            self.df = self.full_df[(self.full_df['Date'] >= monday) & (self.full_df['Date'] <= today)]
        return self.df

    def filter_latest_day(self):
        """Filter data to only include the most recent day in the dataset."""
        if self.full_df is not None and not self.full_df.empty:
            latest_date = self.full_df['Date'].max()
            self.df = self.full_df[self.full_df['Date'] == latest_date]
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
