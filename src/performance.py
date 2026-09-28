import pandas as pd
import math
import matplotlib.pyplot as plt
class PerformanceAnalyzer:

    def __init__(self, data: pd.DataFrame, initial_capital, trades: list):
        self.data = data
        self.equity = data["Equity"]
        self.initial_capital = initial_capital
        self.trades = trades

    def total_return(self):
        return (self.equity.iloc[-1] / self.initial_capital) - 1

    def buy_and_hold_return(self):
        start_price = self.data["Close"].iloc[0]
        end_price = self.data["Close"].iloc[-1]

        return (end_price / start_price) - 1
    
    def daily_returns(self):
        return self.equity.pct_change()

    def sharpe_ratio(self):
        returns = self.daily_returns().dropna()
        if returns.std() == 0:
            return 0.0
        return (returns.mean()/ returns.std()) * (math.sqrt(252))

    def max_drawdown(self):
        peak = self.equity.cummax()
        drawdown = (self.equity - peak) / peak
        return drawdown.min()

    def turnover(self):

        traded_value = sum(
            trade["Quantity"] * trade["Price"]
            for trade in self.trades)

        return traded_value / self.initial_capital

    def summary(self):

        stats = self.trade_stats()

        return {
            "Initial Capital": self.initial_capital,
            "Final Equity": float(self.equity.iloc[-1]),
            "Total Return": float(self.total_return()),
            "Buy & Hold Return": self.buy_and_hold_return(),
            "Sharpe Ratio": float(self.sharpe_ratio()),
            "Max Drawdown": float(self.max_drawdown()),
            "Turnover": float(self.turnover()),
            **stats
        }

    def trade_stats(self):

        closed_trades = [
            trade for trade in self.trades
            if "Net PnL" in trade
        ]

        if not closed_trades:
            return {}

        pnls = [trade["Net PnL"] for trade in closed_trades]

        wins = [pnl for pnl in pnls if pnl > 0]
        losses = [pnl for pnl in pnls if pnl < 0]

        return {
            "Number of Trades": len(pnls),
            "Winning Trades": len(wins),
            "Losing Trades": len(losses),
            "Win Rate": len(wins) / len(pnls),
            "Average Win": float(sum(wins) / len(wins)) if wins else 0,
            "Average Loss": float(sum(losses) / len(losses)) if losses else 0,
            "Profit Factor": (
                float(sum(wins) / abs(sum(losses)))
                if losses else float("inf")
            )
        }

    def plot_equity_curve(self):
        buy_hold_equity = (self.data["Close"] 
                           / self.data["Close"].iloc[0]
                           ) * self.initial_capital
        plt.figure(figsize=(10, 5))

        plt.plot(self.equity.index, self.equity, label="Strategy")
        plt.plot(buy_hold_equity.index, buy_hold_equity, label="Buy & Hold")

        plt.title("Equity Curve")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Equity")

        plt.legend()
        plt.grid(True)
        plt.show()