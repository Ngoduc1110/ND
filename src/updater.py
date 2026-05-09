import shutil
import os
import sys
import pandas as pd
from datetime import datetime

# Add project root to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.processor import DataProcessor
from src.visualizer import Visualizer
from src.analyzer import Analyzer
from src.report_builder import generate_report

# --- CONFIGURATION ---
SOURCE_FILE = r'D:\Dulieuxuatra\NN_TD.csv'
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
TARGET_FILE = os.path.join(PROJECT_DATA_DIR, 'NN_TD.csv')

def sync_data():
    """Sync data from the export folder to the project folder."""
    if not os.path.exists(SOURCE_FILE):
        print(f"[!] Error: Source file not found at {SOURCE_FILE}")
        return False
    
    print(f"[*] Syncing data from {SOURCE_FILE}...")
    try:
        shutil.copy2(SOURCE_FILE, TARGET_FILE)
        print(f"[+] Successfully synced to {TARGET_FILE}")
        return True
    except Exception as e:
        print(f"[!] Sync failed: {e}")
        return False

def run_update_and_analysis():
    """Perform sync and then re-run analysis."""
    if sync_data():
        # Load and verify data
        processor = DataProcessor(TARGET_FILE)
        df = processor.load_data()
        
        # Get latest date
        latest_date = df['Date'].max()
        print(f"[*] Data is up to date as of: {latest_date}")
        
        # Run analysis (Main logic)
        viz = Visualizer(output_dir=os.path.join(PROJECT_ROOT, 'outputs'))
        
        print("[*] Re-generating charts (All Time)...")
        date_str = processor.get_date_range_str()
        
        summary = processor.get_market_summary()
        viz.plot_net_flow(summary, date_range_str=date_str, prefix='all')
        
        nn_buy, nn_sell = processor.get_top_tickers(group='NN')
        viz.plot_top_tickers(nn_buy, nn_sell, group_name='Foreign', date_range_str=date_str, prefix='all')
        
        td_buy, td_sell = processor.get_top_tickers(group='TD')
        viz.plot_top_tickers(td_buy, td_sell, group_name='Proprietary', date_range_str=date_str, prefix='all')
        
        print("[*] Generating charts (Recent Week)...")
        # 1. Generate All-Time insights before filtering
        analyzer = Analyzer(processor)
        all_time_insights = analyzer.generate_insights()

        processor.filter_recent_week()
        week_date_str = processor.get_date_range_str()
        
        # 2. Generate Weekly insights after filtering
        weekly_insights = analyzer.generate_insights()

        weekly_summary = processor.get_market_summary()
        if not weekly_summary.empty:
            viz.plot_net_flow(weekly_summary, date_range_str=week_date_str, prefix='weekly')
            
            w_nn_buy, w_nn_sell = processor.get_top_tickers(group='NN')
            viz.plot_top_tickers(w_nn_buy, w_nn_sell, group_name='Foreign', date_range_str=week_date_str, prefix='weekly')
            
            w_td_buy, w_td_sell = processor.get_top_tickers(group='TD')
            viz.plot_top_tickers(w_td_buy, w_td_sell, group_name='Proprietary', date_range_str=week_date_str, prefix='weekly')
        else:
            print("[!] No data available for the recent week.")
            weekly_insights = "<p>Không có dữ liệu cho tuần gần nhất.</p>"
        
        # Build and update the HTML report
        report_path = os.path.join(PROJECT_ROOT, '..', 'institutional_report.html')
        generate_report(all_time_insights, weekly_insights, report_path)
        
        print(f"\n[SUCCESS] Daily update completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    run_update_and_analysis()
