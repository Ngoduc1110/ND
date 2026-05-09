import pandas as pd

class Analyzer:
    def __init__(self, processor):
        self.processor = processor

    def generate_insights(self):
        """Generate textual insights based on the processor's current data state."""
        df = self.processor.df
        if df is None or df.empty:
            return "<p>Không có dữ liệu để phân tích.</p>"

        # Summary calculations
        total_nn_net = df['GT NN Net'].sum()
        total_td_net = df['GT TD Net'].sum()

        nn_trend = "mua ròng" if total_nn_net > 0 else "bán ròng"
        td_trend = "mua ròng" if total_td_net > 0 else "bán ròng"

        # Format values in billions (Tỷ VNĐ)
        nn_val_bil = abs(total_nn_net) / 1e9
        td_val_bil = abs(total_td_net) / 1e9

        # Get top tickers
        nn_buy, nn_sell = self.processor.get_top_tickers(n=3, group='NN')
        td_buy, td_sell = self.processor.get_top_tickers(n=3, group='TD')

        html_content = f"""
        <div class="insight-box" style="background: rgba(99, 102, 241, 0.1); border-left: 4px solid var(--primary); padding: 1.5rem; border-radius: 8px; margin-bottom: 2rem;">
            <h3 style="color: #fff; margin-bottom: 1rem;">Nhận định Dòng Tiền Tổ Chức:</h3>
            <ul style="color: var(--text-dim); line-height: 1.8; margin-left: 1.5rem;">
                <li><strong>Khối Ngoại (NN):</strong> Đang có xu hướng <strong style="color: {'#10b981' if total_nn_net > 0 else '#ef4444'};">{nn_trend}</strong> với tổng giá trị khoảng <strong>{nn_val_bil:,.1f} tỷ VNĐ</strong>.
                    Các mã được gom mua nhiều nhất là {', '.join(nn_buy.index)}, trong khi bị bán mạnh ở {', '.join(nn_sell.index)}.
                </li>
                <li><strong>Tự Doanh (TD):</strong> Đang có xu hướng <strong style="color: {'#10b981' if total_td_net > 0 else '#ef4444'};">{td_trend}</strong> với tổng giá trị khoảng <strong>{td_val_bil:,.1f} tỷ VNĐ</strong>.
                    Các mã được gom mua nhiều nhất là {', '.join(td_buy.index)}, trong khi bị bán mạnh ở {', '.join(td_sell.index)}.
                </li>
            </ul>
        </div>
        """
        return html_content
