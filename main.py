from src.processor import DataProcessor
from src.visualizer import Visualizer
from src.analyzer import Analyzer
from src.report_builder import generate_report, generate_industry_report
from src.industry_processor import IndustryProcessor
from src.industry_visualizer import IndustryVisualizer
from src.pdf_exporter import export_html_to_pdf
import os

def main():
    # 1. Setup paths
    data_path = os.path.join('data', 'NN_TD.csv')
    output_dir = 'outputs'
    
    if not os.path.exists(data_path):
        print(f"[!] Error: Data file not found at {data_path}")
        return

    # 2. Process Data
    processor = DataProcessor(data_path)
    df = processor.load_data()
    
    market_summary = processor.get_market_summary()
    
    # 3. Generate Visualizations
    viz = Visualizer(output_dir)
    
    print("[*] Generating charts (All Time)...")
    date_str = processor.get_date_range_str()
    
    # Flow history
    viz.plot_net_flow(market_summary, date_range_str=date_str, prefix='all')
    
    # Top Foreign (NN)
    nn_buy, nn_sell = processor.get_top_tickers(group='NN')
    viz.plot_top_tickers(nn_buy, nn_sell, group_name='Foreign', date_range_str=date_str, prefix='all')
    
    # Top Proprietary (TD)
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
    report_path = os.path.join('..', 'institutional_report.html')
    generate_report(all_time_insights, weekly_insights, report_path)
    
    # Export report to PDF for clients
    pdf_path = os.path.join(output_dir, 'institutional_report.pdf')
    export_html_to_pdf(report_path, pdf_path)
    
    # --- 4. Process Industry Indices Data ---
    print("\n[*] Processing Industry Indices (CHISONGANH.csv)...")
    industry_data_path = r'D:\dulieuxuatra\CHISONGANH.csv'
    if not os.path.exists(industry_data_path):
        print(f"[!] Warning: Industry data file not found at {industry_data_path}")
    else:
        ind_processor = IndustryProcessor(industry_data_path)
        ind_df = ind_processor.load_data()
        
        recent_ind_df = ind_processor.get_recent_data(months=3)
        top_industries = ind_processor.get_top_industries(recent_ind_df, top_n=5)
        
        ind_viz = IndustryVisualizer(output_dir)
        vol_chart_html = ind_viz.plot_volume_bar(recent_ind_df, top_industries)
        
        candlestick_htmls = []
        for ind in top_industries:
            ch = ind_viz.plot_candlestick(recent_ind_df, ind)
            candlestick_htmls.append(ch)
            
        industry_report_path = os.path.join('..', 'industry_report.html')
        generate_industry_report(vol_chart_html, candlestick_htmls, industry_report_path)
        print(f"[+] Generated Industry Indices report at {industry_report_path}")

    print(f"\n[SUCCESS] Analysis complete! Check the '{output_dir}' folder for results.")

if __name__ == "__main__":
    main()
