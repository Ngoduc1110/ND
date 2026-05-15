import pandas as pd

class Analyzer:
    def __init__(self, processor):
        self.processor = processor

    def generate_insights(self):
        """Generate textual insights based on the processor's current data state."""
        df = self.processor.df
        if df is None or df.empty:
            return "<div class='insight-box'>Không có dữ liệu cho giai đoạn này.</div>"

        # Summary calculations
        total_nn_net = df['GT NN Net'].sum()
        total_td_net = df['GT TD Net'].sum()

        nn_trend = "mua ròng" if total_nn_net > 0 else "bán ròng"
        td_trend = "mua ròng" if total_td_net > 0 else "bán ròng"

        # Format values in billions (Tỷ VNĐ)
        # Note: Input values in NN_TD.csv are assumed to be in 1,000 VND units
        nn_val_bil = abs(total_nn_net) / 1e6
        td_val_bil = abs(total_td_net) / 1e6

        # Get top tickers
        nn_all_buy, nn_all_sell = self.processor.get_top_tickers(n=10, group='NN')
        td_all_buy, td_all_sell = self.processor.get_top_tickers(n=10, group='TD')
        
        # Filter to ensure buy is positive and sell is negative
        nn_buy_clean = nn_all_buy[nn_all_buy > 0].head(3)
        nn_sell_clean = nn_all_sell[nn_all_sell < 0].head(3)
        td_buy_clean = td_all_buy[td_all_buy > 0].head(3)
        td_sell_clean = td_all_sell[td_all_sell < 0].head(3)

        def format_list(s):
            if s.empty: return "không có"
            return ", ".join(s.index)

        html_content = f"""
        <div class="insight-box" style="background: rgba(99, 102, 241, 0.1); border-left: 4px solid var(--primary); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
            <h3 style="color: #fff; margin-bottom: 1rem;">Nhận định Dòng Tiền Tổ Chức:</h3>
            <ul style="color: var(--text-dim); line-height: 1.8; margin-left: 1.5rem;">
                <li><strong>Khối Ngoại (NN):</strong> Đang có xu hướng <strong style="color: {'#10b981' if total_nn_net > 0 else '#ef4444'};">{nn_trend}</strong> với tổng giá trị khoảng <strong>{nn_val_bil:,.1f} tỷ VNĐ</strong>.
                    Các mã được gom mua nhiều nhất là {format_list(nn_buy_clean)}, trong khi bị bán mạnh ở {format_list(nn_sell_clean)}.
                </li>
                <li><strong>Tự Doanh (TD):</strong> Đang có xu hướng <strong style="color: {'#10b981' if total_td_net > 0 else '#ef4444'};">{td_trend}</strong> với tổng giá trị khoảng <strong>{td_val_bil:,.1f} tỷ VNĐ</strong>.
                    Các mã được gom mua nhiều nhất là {format_list(td_buy_clean)}, trong khi bị bán mạnh ở {format_list(td_sell_clean)}.
                </li>
            </ul>
        </div>
        """
        return html_content
