import matplotlib.pyplot as plt
import seaborn as sns
import os

class Visualizer:
    def __init__(self, output_dir='outputs'):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Set style
        sns.set_theme(style="whitegrid")

    def plot_net_flow(self, summary_df, date_range_str="", prefix=""):
        """Plot Foreign vs Proprietary net flow over time."""
        plt.figure(figsize=(14, 7))
        
        plt.plot(summary_df['Date'], summary_df['GT NN Net'], label='Foreign (NN) Net', color='blue', linewidth=2)
        plt.plot(summary_df['Date'], summary_df['GT TD Net'], label='Proprietary (TD) Net', color='orange', linewidth=2)
        
        plt.axhline(0, color='red', linestyle='--', alpha=0.5)
        
        title = 'Vietnam Stock Market: Net Trading Value (Foreign vs Proprietary)'
        if date_range_str:
            title += f'\n({date_range_str})'
        plt.title(title, fontsize=16)
        
        plt.xlabel('Date')
        plt.ylabel('Net Value (VND)')
        plt.legend()
        
        file_name = f'{prefix}_net_flow_history.png' if prefix else 'net_flow_history.png'
        save_path = os.path.join(self.output_dir, file_name)
        plt.savefig(save_path)
        plt.close()
        print(f"[+] Saved flow chart to {save_path}")

    def plot_top_tickers(self, top_buy, top_sell, group_name='Foreign', date_range_str="", prefix=""):
        """Plot top tickers for a specific group."""
        fig, axes = plt.subplots(1, 2, figsize=(16, 8))
        
        # Top Buy
        sns.barplot(x=top_buy.values, y=top_buy.index, ax=axes[0], hue=top_buy.index, palette='viridis', legend=False)
        title_buy = f'Top 10 {group_name} Net Buy'
        if date_range_str:
            title_buy += f'\n({date_range_str})'
        axes[0].set_title(title_buy, fontsize=14)
        
        # Top Sell
        sns.barplot(x=top_sell.values, y=top_sell.index, ax=axes[1], hue=top_sell.index, palette='magma', legend=False)
        title_sell = f'Top 10 {group_name} Net Sell'
        if date_range_str:
            title_sell += f'\n({date_range_str})'
        axes[1].set_title(title_sell, fontsize=14)
        
        plt.tight_layout()
        file_name = f'{prefix}_top_tickers_{group_name.lower()}.png' if prefix else f'top_tickers_{group_name.lower()}.png'
        save_path = os.path.join(self.output_dir, file_name)
        plt.savefig(save_path)
        plt.close()
        print(f"[+] Saved top tickers chart to {save_path}")
