import pandas as pd


class MovingAverageStrategy:

    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def prepare_indicators(self, data: pd.DataFrame):
        df = data.copy()
        df["Short_MA"] = df["Close"].rolling(self.short_window).mean()
        df["Long_MA"] = df["Close"].rolling(self.long_window).mean()

        df["Raw_Signal"] = (df["Short_MA"] > df["Long_MA"]).astype(int)

        df.iloc[: self.long_window - 1, df.columns.get_loc("Raw_Signal")] = 0
        return df
