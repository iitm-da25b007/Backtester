class PercentageOfEquitySizer:

    def __init__(self, percentage):
        self.percentage = percentage

    def get_target_position(self, signal, equity, price):

        if signal == 0:
            return 0

        capital = equity * self.percentage

        quantity = int(capital // price)

        return quantity
