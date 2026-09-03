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

    def run(self):

        pending_order = None

        for i in range(len(self.data)):

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
                        "Price": execution_price
                    }

                    if quantity > 0:
                        self.entry_price = execution_price

                    elif quantity < 0:

                        pnl = (
                            execution_price - self.entry_price
                        ) * abs(quantity)

                        trade["PnL"] = pnl

                        self.entry_price = None

                    self.trades.append(trade)

                pending_order = None

            # Calculate equity
            self.data.loc[
                self.data.index[i], "Equity"
            ] = self.portfolio.update_equity(
                self.data["Close"].iloc[i]
            )

            # Generate signal
            signal = self.strategy.generate_signal(
                self.data.iloc[:i + 1]
            )

            equity = self.portfolio.update_equity(
                self.data["Close"].iloc[i]
            )

            target = self.sizer.get_target_position(
                signal,
                equity,
                self.data["Close"].iloc[i]
            )
            
            quantity = target - self.portfolio.position

            # Schedule order for next day's open
            if quantity != 0 and i + 1 < len(self.data):
                pending_order = quantity

        # Final equity
        self.data.loc[
            self.data.index[-1], "Equity"
        ] = self.portfolio.update_equity(
            self.data["Close"].iloc[-1]
        )

        return self.data