import pandas as pd

from src.backtester import Backtester
from src.strategy import MovingAverageStrategy
from src.portfolio import Portfolio
from src.position_sizer import PercentageOfEquitySizer


def test_order_executes_on_next_day_open():

    data = pd.DataFrame(
        {
            "Open": [100, 101, 102, 103, 104],
            "High": [105, 106, 107, 108, 109],
            "Low": [95, 96, 97, 98, 99],
            "Close": [100, 101, 102, 103, 104],
            "Volume": [1000, 1000, 1000, 1000, 1000],
        }
    )

    strategy = MovingAverageStrategy(short_window=2, long_window=3)

    portfolio = Portfolio(1000)

    sizer = PercentageOfEquitySizer(1.0)

    backtester = Backtester(data, strategy, portfolio, sizer)

    backtester.run()

    assert backtester.trades[0]["Price"] == 103


def test_trade_pnl():

    data = pd.DataFrame(
        {
            "Open": [100, 100, 110, 120, 90, 80],
            "High": [105, 105, 115, 125, 95, 85],
            "Low": [95, 95, 105, 115, 85, 75],
            "Close": [100, 100, 110, 120, 90, 80],
            "Volume": [1000, 1000, 1000, 1000, 1000, 1000],
        }
    )

    strategy = MovingAverageStrategy(short_window=2, long_window=3)

    portfolio = Portfolio(1000)
    sizer = PercentageOfEquitySizer(0.5)

    backtester = Backtester(data, strategy, portfolio, sizer)

    backtester.run()

    buy_trade = backtester.trades[0]
    sell_trade = backtester.trades[1]

    assert buy_trade["Action"] == "BUY"
    assert sell_trade["Action"] == "SELL"
    assert sell_trade["Net PnL"] < 0


def test_position_size_uses_signal_day_close():

    data = pd.DataFrame(
        {
            "Open": [100, 100, 200, 200],
            "High": [105, 105, 205, 205],
            "Low": [95, 95, 195, 195],
            "Close": [100, 110, 120, 130],
            "Volume": [1000, 1000, 1000, 1000],
        }
    )

    strategy = MovingAverageStrategy(short_window=1, long_window=2)

    portfolio = Portfolio(1000)
    sizer = PercentageOfEquitySizer(0.5)

    backtester = Backtester(data, strategy, portfolio, sizer)

    backtester.run()

    trade = backtester.trades[0]

    assert trade["Action"] == "BUY"
    assert trade["Price"] == 200
    assert trade["Quantity"] == 4


def test_multiple_buys_use_average_entry_price():

    class FixedSignalStrategy:

        def prepare_indicators(self, data):
            df = data.copy()
            df["Raw_Signal"] = [1 if i < 3 else 0 for i in range(len(df))]
            return df

    class FixedSizer:

        def get_target_position(self, signal, equity, price):
            if signal == 1:
                if price == 100:
                    return 10
                return 12

            return 0

    data = pd.DataFrame(
        {
            "Open": [100, 100, 110, 120, 130],
            "High": [105, 105, 115, 125, 135],
            "Low": [95, 95, 105, 115, 125],
            "Close": [100, 100, 110, 120, 130],
            "Volume": [1000, 1000, 1000, 1000, 1000],
        }
    )

    strategy = FixedSignalStrategy()
    portfolio = Portfolio(5000, transaction_cost=0.0, slippage=0.0)
    sizer = FixedSizer()

    backtester = Backtester(data, strategy, portfolio, sizer)

    backtester.run()

    buy_1 = backtester.trades[0]
    buy_2 = backtester.trades[1]
    sell_trade = backtester.trades[2]

    assert buy_1["Action"] == "BUY"
    assert buy_1["Quantity"] == 10

    assert buy_2["Action"] == "BUY"
    assert buy_2["Quantity"] == 2

    assert sell_trade["Action"] == "SELL"
    assert sell_trade["Quantity"] == 12
    assert sell_trade["Gross PnL"] > 0
