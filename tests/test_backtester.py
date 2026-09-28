import pandas as pd

from src.backtester import Backtester
from src.strategy import MovingAverageStrategy
from src.portfolio import Portfolio
from src.position_sizer import PercentageOfEquitySizer

def test_order_executes_on_next_day_open():

    data = pd.DataFrame({
        "Open": [100, 101, 102, 103, 104],
        "High": [105, 106, 107, 108, 109],
        "Low": [95, 96, 97, 98, 99],
        "Close": [100, 101, 102, 103, 104],
        "Volume": [1000, 1000, 1000, 1000, 1000]
    })

    strategy = MovingAverageStrategy(
        short_window=2,
        long_window=3
    )

    portfolio = Portfolio(1000)

    sizer = PercentageOfEquitySizer(1.0)

    backtester = Backtester(
        data,
        strategy,
        portfolio,
        sizer
    )

    backtester.run()

    assert backtester.trades[0]["Price"] == 103

def test_trade_pnl():

    data = pd.DataFrame({
        "Open": [100, 100, 110, 120, 90, 80],
        "High": [105, 105, 115, 125, 95, 85],
        "Low": [95, 95, 105, 115, 85, 75],
        "Close": [100, 100, 110, 120, 90, 80],
        "Volume": [1000, 1000, 1000, 1000, 1000, 1000]
    })

    strategy = MovingAverageStrategy(
        short_window=2,
        long_window=3
    )

    portfolio = Portfolio(1000)
    sizer = PercentageOfEquitySizer(0.5)

    backtester = Backtester(
        data,
        strategy,
        portfolio,
        sizer
    )

    backtester.run()

    buy_trade = backtester.trades[0]
    sell_trade = backtester.trades[1]

    assert buy_trade["Action"] == "BUY"
    assert sell_trade["Action"] == "SELL"
    assert sell_trade["Net PnL"] < 0

def test_position_size_uses_execution_open():

    data = pd.DataFrame({
        "Open": [100, 100, 200, 200],
        "High": [105, 105, 205, 205],
        "Low": [95, 95, 195, 195],
        "Close": [100, 110, 120, 130],
        "Volume": [1000, 1000, 1000, 1000]
    })

    strategy = MovingAverageStrategy(
        short_window=1,
        long_window=2
    )

    portfolio = Portfolio(1000)
    sizer = PercentageOfEquitySizer(0.5)

    backtester = Backtester(
        data,
        strategy,
        portfolio,
        sizer
    )

    backtester.run()

    trade = backtester.trades[0]

    assert trade["Action"] == "BUY"
    assert trade["Price"] == 200
    assert trade["Quantity"] == 2