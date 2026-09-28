from src.portfolio import Portfolio

def test_buy_order():

    portfolio = Portfolio(20000)

    status = portfolio.execute_order(10, 100)

    assert status == "FILLED"
    assert portfolio.position == 10
    assert portfolio.cash == 18999

def test_insufficient_cash():

    portfolio = Portfolio(1000)

    status = portfolio.execute_order(20, 100)

    assert status == "REJECTED"
    assert portfolio.position == 0
    assert portfolio.cash == 1000

def test_sell_order():

    portfolio = Portfolio(20000)

    portfolio.execute_order(10, 100)

    status = portfolio.execute_order(-10, 110)

    assert status == "FILLED"
    assert portfolio.position == 0
    assert portfolio.cash == 20097.9

def test_insufficient_position():

    portfolio = Portfolio(20000)

    portfolio.execute_order(5, 100)

    status = portfolio.execute_order(-10, 110)

    assert status == "REJECTED"
    assert portfolio.position == 5

def test_transaction_cost():

    portfolio = Portfolio(20000, transaction_cost=0.001)

    portfolio.execute_order(10, 100)

    assert portfolio.cash == 18999