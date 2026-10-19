from src.strategy import MovingAverageStrategy
import pandas as pd


def test_prepare_indicators():
    strategy = MovingAverageStrategy(short_window=3, long_window=5)

    data = pd.DataFrame({"Close": [100, 100, 100, 110, 120]})

    result = strategy.prepare_indicators(data)

    assert "Short_MA" in result.columns
    assert "Long_MA" in result.columns
    assert "Raw_Signal" in result.columns
    assert result["Raw_Signal"].iloc[-1] == 1


def test_insufficient_data():
    strategy = MovingAverageStrategy(short_window=3, long_window=5)

    data = pd.DataFrame({"Close": [100, 101, 102, 103]})

    result = strategy.prepare_indicators(data)

    assert (result["Raw_Signal"] == 0).all()


def test_short_ma_below_long_ma():
    strategy = MovingAverageStrategy(short_window=3, long_window=5)

    data = pd.DataFrame({"Close": [120, 120, 120, 110, 100]})

    result = strategy.prepare_indicators(data)

    assert result["Raw_Signal"].iloc[-1] == 0
