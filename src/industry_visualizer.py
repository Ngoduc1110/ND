import plotly.graph_objects as go
import os

class IndustryVisualizer:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def plot_candlestick(self, df, industry_name):
        """
        Generate a candlestick chart using plotly and return the HTML string.
        """
        # Filter the dataframe for the specific industry
        industry_df = df[df['Ten Cty'] == industry_name].copy()
        
        if industry_df.empty:
            return f"<p>No data available for {industry_name}</p>"

        # Sort by date just in case
        industry_df = industry_df.sort_values(by='Date/Time')

        fig = go.Figure(data=[go.Candlestick(
            x=industry_df['Date/Time'],
            open=industry_df['Open'],
            high=industry_df['High'],
            low=industry_df['Low'],
            close=industry_df['Close'],
            name=industry_name
        )])

        fig.update_layout(
            title=f"Biến Động Nến - Ngành {industry_name}",
            yaxis_title='Điểm số / Giá',
            xaxis_title='Thời gian',
            template='plotly_dark',
            margin=dict(l=40, r=40, t=60, b=40),
            height=500
        )

        # Disable range slider for a cleaner look
        fig.update_layout(xaxis_rangeslider_visible=False)

        # Generate the HTML snippet (include plotly JS if it's the first time, 
        # but to be safe we'll use include_plotlyjs='cdn' or let the main HTML handle it)
        # using 'cdn' inside each div is fine, or we can just return a div and include CDN in header.
        html_div = fig.to_html(full_html=False, include_plotlyjs=False)
        return html_div

    def plot_volume_bar(self, df, top_industries):
        """
        Generate a bar chart for volume comparison.
        """
        volume_df = df[df['Ten Cty'].isin(top_industries)].groupby('Ten Cty')['Volume'].sum().reset_index()
        volume_df = volume_df.sort_values(by='Volume', ascending=False)
        
        fig = go.Figure(data=[go.Bar(
            x=volume_df['Ten Cty'],
            y=volume_df['Volume'],
            marker_color='#6366f1'
        )])

        fig.update_layout(
            title="Tổng Khối Lượng Giao Dịch (Top 5 Ngành)",
            yaxis_title='Khối lượng',
            template='plotly_dark',
            margin=dict(l=40, r=40, t=60, b=40),
            height=400
        )

        return fig.to_html(full_html=False, include_plotlyjs=False)
