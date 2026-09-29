import pandas as pd
from src.strategy import MovingAverageStrategy
from src.portfolio import Portfolio
from src.position_sizer import PercentageOfEquitySizer

class Backtester:

    def __init__(self, data: pd.DataFrame, strategy: MovingAverageStrategy, portfolio: Portfolio, sizer: PercentageOfEquitySizer):
        self.data = data.copy()
        self.strategy = strategy
        self.portfolio = portfolio
        self.sizer = sizer
        self.trades = []
        self.data["Equity"] = 0.0
        self.entry_price = None
        self.entry_cost = None

    def run(self):

        pending_order = None

        for i in range(len(self.data)):

            # Execute pending order at today's Open
            if pending_order is not None:

                quantity = pending_order
                execution_price = self.data["Open"].iloc[i]

                status = self.portfolio.execute_order(
                    quantity,
                    execution_price
                )

                if status == "FILLED":

                    trade = {
                        "Date": self.data.index[i],
                        "Action": "BUY" if quantity > 0 else "SELL",
                        "Quantity": abs(quantity),
                        "Price": float(execution_price)
                    }

                    if quantity > 0:

                        self.entry_price = execution_price
                        self.entry_cost = (
                            quantity
                            * execution_price
                            * self.portfolio.transaction_cost
                        )

                    elif quantity < 0:

                        gross_pnl = (
                            execution_price
                            - self.entry_price
                        ) * abs(quantity)

                        exit_cost = (
                            abs(quantity)
                            * execution_price
                            * self.portfolio.transaction_cost
                        )

                        transaction_cost = (self.entry_cost + exit_cost)

                        net_pnl = (gross_pnl - transaction_cost)

                        trade["Gross PnL"] = float(gross_pnl)
                        trade["Transaction Cost"] = float(transaction_cost)
                        trade["Net PnL"] = float(net_pnl)

                        self.entry_price = None
                        self.entry_cost = None

                    self.trades.append(trade)

                pending_order = None

            # Calculate end-of-day equity
            self.data.loc[
                self.data.index[i],
                "Equity"
            ] = self.portfolio.update_equity(
                self.data["Close"].iloc[i]
            )

            # Generate today's signal
            signal = self.strategy.generate_signal(
                self.data.iloc[:i + 1]
            )

            # Calculate position at today's Close
            equity = self.portfolio.update_equity(
                self.data["Close"].iloc[i]
            )

            target = self.sizer.get_target_position(
                signal,
                equity,
                self.data["Close"].iloc[i]
            )

            quantity = (target - self.portfolio.position)

            # Schedule order for tomorrow's Open
            if quantity != 0 and i + 1 < len(self.data):
                pending_order = quantity

        # Final equity
        self.data.loc[
            self.data.index[-1],
            "Equity"
        ] = self.portfolio.update_equity(
            self.data["Close"].iloc[-1]
        )

        return self.data