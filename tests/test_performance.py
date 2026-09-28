import pandas as pd
import pytest
from src.performance import PerformanceAnalyzer

def test_total_return():

    data = pd.DataFrame({
        "Close": [100, 105, 110],
        "Equity": [10000, 10500, 11000]
    })

    analyzer = PerformanceAnalyzer(
        data,
        10000,
        []
    )

    result = analyzer.total_return()

    assert result == pytest.approx(0.10)

def test_buy_and_hold_return():

    data = pd.DataFrame({
        "Close": [100, 105, 110],
        "Equity": [10000, 10000, 10000]
    })

    analyzer = PerformanceAnalyzer(
        data,
        10000,
        []
    )

    result = analyzer.buy_and_hold_return()

    assert result == pytest.approx(0.10)

def test_max_drawdown():

    data = pd.DataFrame({
        "Close": [100, 105, 100, 110],
        "Equity": [10000, 12000, 9000, 11000]
    })

    analyzer = PerformanceAnalyzer(
        data,
        10000,
        []
    )

    result = analyzer.max_drawdown()

    assert result == pytest.approx(-0.25)

def test_trade_stats():

    data = pd.DataFrame({
        "Close": [100, 110],
        "Equity": [10000, 10100]
    })

    trades = [
        {"Net PnL": 100},
        {"Net PnL": -50},
        {"Net PnL": 200}
    ]

    analyzer = PerformanceAnalyzer(
        data,
        10000,
        trades
    )

    stats = analyzer.trade_stats()

    assert stats["Number of Trades"] == 3
    assert stats["Winning Trades"] == 2
    assert stats["Losing Trades"] == 1
    assert stats["Win Rate"] == pytest.approx(2 / 3)
    assert stats["Average Win"] == pytest.approx(150)
    assert stats["Average Loss"] == pytest.approx(-50)
    assert stats["Profit Factor"] == pytest.approx(6)