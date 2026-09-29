from src.data_loader import load_data
from src.strategy import MovingAverageStrategy
from src.portfolio import Portfolio
from src.backtester import Backtester
from src.performance import PerformanceAnalyzer
from src.position_sizer import PercentageOfEquitySizer


df = load_data(
    "RELIANCE.NS",
    "2024-01-01",
    "2025-01-01"
)

strategy = MovingAverageStrategy(
    short_window=20,
    long_window=50
)
portfolio = Portfolio(20000,slippage=0.001)

sizer = PercentageOfEquitySizer(1.0)

backtester = Backtester(
    df,
    strategy,
    portfolio,
    sizer
)

results = backtester.run()

analyzer = PerformanceAnalyzer(
    results,
    portfolio.initial_cash,
    backtester.trades
)

summary = analyzer.summary()

print(summary)

analyzer.plot_equity_curve()