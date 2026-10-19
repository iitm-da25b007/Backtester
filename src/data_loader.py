import yfinance as yf


def load_data(ticker, start, end):

    data = yf.download(ticker, start=start, end=end, auto_adjust=False)

    data = data.droplevel("Ticker", axis=1)

    data = data[["Open", "High", "Low", "Close", "Volume"]]

    data = data.sort_index()

    data = data[~data.index.duplicated(keep="first")]

    data = data.dropna()

    if data.empty:
        raise ValueError("No valid data available")

    if data.isna().any().any():
        raise ValueError("Missing values remain")

    if not data.index.is_unique:
        raise ValueError("Duplicate dates remain")

    if not data.index.is_monotonic_increasing:
        raise ValueError("Dates are not sorted")

    return data
