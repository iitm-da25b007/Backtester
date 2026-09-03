class Portfolio:

    def __init__(self, initial_cash, transaction_cost=0.001):
        self.cash = initial_cash
        self.position = 0
        self.initial_cash = initial_cash
        self.transaction_cost = transaction_cost

    def execute_order(self, quantity, price):

        trade_value = abs(quantity) * price
        cost = trade_value * self.transaction_cost

        if quantity > 0:

            total = trade_value + cost

            if total > self.cash:
                return "REJECTED"

            self.cash -= total

        if quantity < 0:

            if abs(quantity) > self.position:
                return "REJECTED"

            self.cash += trade_value - cost

        self.position += quantity

        return "FILLED"

    def update_equity(self, price):
        return self.cash + self.position * price