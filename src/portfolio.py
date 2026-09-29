class Portfolio:

    def __init__(self, initial_cash, transaction_cost=0.001, slippage=0.0):
        self.cash = initial_cash
        self.position = 0
        self.initial_cash = initial_cash
        self.transaction_cost = transaction_cost
        self.slippage = slippage

    def execute_order(self, quantity, price):

        if quantity > 0:
            execution_price = price * (1 + self.slippage)
        else:
            execution_price = price * (1 - self.slippage)

        trade_value = abs(quantity) * execution_price
        cost = trade_value * self.transaction_cost

        if quantity > 0:

            total = trade_value + cost

            if total > self.cash:
                return "REJECTED", None

            self.cash -= total

        if quantity < 0:

            if abs(quantity) > self.position:
                return "REJECTED", None

            self.cash += trade_value - cost

        self.position += quantity

        return "FILLED", execution_price

    def update_equity(self, price):
        return self.cash + self.position * price