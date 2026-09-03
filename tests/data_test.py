from src.data_loader import load_data
from src.strategy import MovingAverageStrategy
from src.portfolio import Portfolio
from src.backtester import Backtester
from src.performance import PerformanceAnalyzer


df = load_data(
    "RELIANCE.NS",
    "2024-01-01",
    "2025-01-01"
)

strategy = MovingAverageStrategy(
    short_window=20,
    long_window=50
)
portfolio = Portfolio(2000)

backtester = Backtester(
    df,
    strategy,
    portfolio
)

results = backtester.run()

analyzer = PerformanceAnalyzer(
    results["Equity"],
    portfolio.initial_cash,
    backtester.trades
)

print(results)
print(backtester.trades)
print(analyzer.summary())