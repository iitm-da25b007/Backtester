class MovingAverageStrategy:

    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, data):

        if len(data) < self.long_window:
            return 0

        short_ma = data["Close"].rolling(
            self.short_window
        ).mean()

        long_ma = data["Close"].rolling(
            self.long_window
        ).mean()

        if short_ma.iloc[-1] > long_ma.iloc[-1]:
            return 1

        return 0