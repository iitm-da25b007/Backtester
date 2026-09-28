import pandas as pd
import math
class PerformanceAnalyzer:

    def __init__(self, equity: pd.Series, initial_capital, trades: dict):
        self.equity = equity
        self.initial_capital = initial_capital
        self.trades = trades

    def total_return(self):
        return (self.equity.iloc[-1] / self.initial_capital) - 1

    
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

        stats = self.trade_stats(self.trades)

        return {
            "Initial Capital": self.initial_capital,
            "Final Equity": float(self.equity.iloc[-1]),
            "Total Return": float(self.total_return()),
            "Sharpe Ratio": float(self.sharpe_ratio()),
            "Max Drawdown": float(self.max_drawdown()),
            "Turnover": float(self.turnover()),
            **stats
        }

    def trade_stats(self, trades):

        closed_trades = [
            trade for trade in trades
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