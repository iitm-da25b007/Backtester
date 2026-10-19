import pandas as pd
from src.strategy import MovingAverageStrategy
from src.portfolio import Portfolio
from src.position_sizer import PercentageOfEquitySizer


class Backtester:

    def __init__(
        self,
        data: pd.DataFrame,
        strategy: MovingAverageStrategy,
        portfolio: Portfolio,
        sizer: PercentageOfEquitySizer,
    ):
        self.data = strategy.prepare_indicators(data)
        self.portfolio = portfolio
        self.sizer = sizer
        self.trades = []
        self.data["Equity"] = 0.0
        self.entry_price = None
        self.entry_cost = 0.0

    def run(self):
        pending_order = None

        for i in range(len(self.data)):
            # Execute pending order at today's Open
            if pending_order is not None:
                quantity = pending_order
                execution_price = self.data["Open"].iloc[i]

                status, fill_price = self.portfolio.execute_order(
                    quantity, execution_price
                )

                if status == "FILLED":
                    trade = {
                        "Date": self.data.index[i],
                        "Action": "BUY" if quantity > 0 else "SELL",
                        "Quantity": abs(quantity),
                        "Price": float(fill_price),
                    }

                    if quantity > 0:
                        buy_value = quantity * fill_price
                        buy_cost = buy_value * self.portfolio.transaction_cost

                        if self.portfolio.position - quantity > 0:
                            old_position = self.portfolio.position - quantity
                            total_position_value = (
                                old_position * self.entry_price + buy_value
                            )
                            self.entry_price = (
                                total_position_value / self.portfolio.position
                            )
                            self.entry_cost += buy_cost
                        else:
                            self.entry_price = fill_price
                            self.entry_cost = buy_cost

                    elif quantity < 0:
                        sell_quantity = abs(quantity)
                        gross_pnl = (fill_price - self.entry_price) * sell_quantity
                        exit_cost = (
                            sell_quantity * fill_price * self.portfolio.transaction_cost
                        )
                        entry_cost_per_share = self.entry_cost / (
                            self.portfolio.position + sell_quantity
                        )
                        entry_cost_for_trade = entry_cost_per_share * sell_quantity
                        transaction_cost = entry_cost_for_trade + exit_cost
                        net_pnl = gross_pnl - transaction_cost

                        trade["Gross PnL"] = float(gross_pnl)
                        trade["Transaction Cost"] = float(transaction_cost)
                        trade["Net PnL"] = float(net_pnl)

                        self.entry_cost -= entry_cost_for_trade

                        if self.portfolio.position == 0:
                            self.entry_price = None
                            self.entry_cost = 0.0

                    self.trades.append(trade)
                pending_order = None

            self.data.loc[self.data.index[i], "Equity"] = self.portfolio.update_equity(
                self.data["Close"].iloc[i]
            )

            signal = self.data["Raw_Signal"].iloc[i]

            # Calculate position at today's Close
            equity = self.portfolio.update_equity(self.data["Close"].iloc[i])
            target = self.sizer.get_target_position(
                signal, equity, self.data["Close"].iloc[i]
            )
            quantity = target - self.portfolio.position

            # Schedule order for tomorrow's Open
            if quantity != 0 and i + 1 < len(self.data):
                pending_order = quantity

        # Final equity
        self.data.loc[self.data.index[-1], "Equity"] = self.portfolio.update_equity(
            self.data["Close"].iloc[-1]
        )
        return self.data
