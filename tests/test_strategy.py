from src.strategy import MovingAverageStrategy
import pandas as pd

def test_not_enough_data():

    strategy = MovingAverageStrategy(
        short_window=3,
        long_window=5
    )

    data = pd.DataFrame({
        "Close": [100, 101, 102, 103]
    })

    signal = strategy.generate_signal(data)

    assert signal == 0

def test_buy_signal():

    strategy = MovingAverageStrategy(
        short_window=3,
        long_window=5
    )

    data = pd.DataFrame({
        "Close": [100, 100, 100, 110, 120]
    })

    signal = strategy.generate_signal(data)

    assert signal == 1

def test_no_buy_signal():

    strategy = MovingAverageStrategy(
        short_window=3,
        long_window=5
    )

    data = pd.DataFrame({
        "Close": [120, 110, 100, 100, 100]
    })

    signal = strategy.generate_signal(data)

    assert signal == 0