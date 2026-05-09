import os
from src.analyzer import Analyzer

def generate_report(all_time_insights, weekly_insights, output_path):
    """Generate the full HTML report with embedded analysis."""

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo Cáo Giao Dịch Tổ Chức</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f1f5f9;
            --text-dim: #94a3b8;
            --primary: #6366f1;
            --accent: #818cf8;
            --border: #334155;
        }}
        
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Inter', sans-serif; 
            background-color: var(--bg); 
            color: var(--text);
            line-height: 1.6;
            padding: 2rem;
        }}
        
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        header {{ 
            margin-bottom: 2rem; 
            text-align: center;
            background: linear-gradient(135deg, #1e1b4b 0%, #1e293b 100%);
            padding: 2rem;
            border-radius: 24px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
            border: 1px solid var(--border);
        }}

        .tabs {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}

        .tabs a {{
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            color: var(--text-dim);
            background: var(--card-bg);
            border: 1px solid var(--border);
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .tabs a:hover {{
            color: #fff;
            border-color: var(--primary);
        }}

        .tabs a.active {{
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }}
        
        h1 {{ font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        
        .section-title {{
            font-size: 1.5rem;
            margin: 3rem 0 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border);
            color: #fff;
        }}
        
        .chart-container {{
            background: #fff;
            border-radius: 16px;
            padding: 1rem;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
            overflow: hidden;
        }}

        .chart-container img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            display: block;
        }}
        
        .footer {{ margin-top: 4rem; text-align: center; color: var(--text-dim); font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="tabs">
            <a href="index.html">News Dashboard</a>
            <a href="institutional_report.html" class="active">Institutional Trading</a>
        </div>

        <header>
            <h1>Báo Cáo Giao Dịch Tổ Chức</h1>
            <p style="color: var(--text-dim);">Dữ liệu cập nhật tự động từ hệ thống ND-githup</p>
        </header>

        <h2 class="section-title">1. Báo Cáo Tuần Gần Nhất</h2>
        {weekly_insights}
        <div class="chart-container">
            <img src="ND-githup/outputs/weekly_net_flow_history.png" alt="Weekly Net Flow">
        </div>
        <div class="chart-container">
            <img src="ND-githup/outputs/weekly_top_tickers_foreign.png" alt="Weekly Top Tickers Foreign">
        </div>
        <div class="chart-container">
            <img src="ND-githup/outputs/weekly_top_tickers_proprietary.png" alt="Weekly Top Tickers Proprietary">
        </div>

        <h2 class="section-title">2. Báo Cáo Toàn Thời Gian</h2>
        {all_time_insights}
        <div class="chart-container">
            <img src="ND-githup/outputs/all_net_flow_history.png" alt="All Time Net Flow">
        </div>
        <div class="chart-container">
            <img src="ND-githup/outputs/all_top_tickers_foreign.png" alt="All Time Top Tickers Foreign">
        </div>
        <div class="chart-container">
            <img src="ND-githup/outputs/all_top_tickers_proprietary.png" alt="All Time Top Tickers Proprietary">
        </div>

        <footer class="footer">
            <p>&copy; 2026 Vibecoding Analysis System</p>
        </footer>
    </div>
</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[*] Generated full report at {output_path}")
