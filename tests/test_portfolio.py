from src.portfolio import Portfolio
import pytest


def test_buy_order():

    portfolio = Portfolio(20000)

    status, fill_price = portfolio.execute_order(10, 100)

    assert status == "FILLED"
    assert fill_price == 100.0
    assert portfolio.position == 10
    assert portfolio.cash == 18999


def test_insufficient_cash():

    portfolio = Portfolio(1000)

    status, fill_price = portfolio.execute_order(20, 100)

    assert status == "REJECTED"
    assert fill_price is None
    assert portfolio.position == 0
    assert portfolio.cash == 1000


def test_sell_order():

    portfolio = Portfolio(20000)

    portfolio.execute_order(10, 100)

    status, fill_price = portfolio.execute_order(-10, 110)

    assert status == "FILLED"
    assert fill_price == 110.0
    assert portfolio.position == 0
    assert portfolio.cash == 20097.9


def test_insufficient_position():

    portfolio = Portfolio(20000)

    portfolio.execute_order(5, 100)

    status, fill_price = portfolio.execute_order(-10, 110)

    assert status == "REJECTED"
    assert fill_price is None
    assert portfolio.position == 5


def test_transaction_cost():

    portfolio = Portfolio(20000, transaction_cost=0.001)

    portfolio.execute_order(10, 100)

    assert portfolio.cash == 18999


def test_buy_with_slippage():

    portfolio = Portfolio(20000, transaction_cost=0.0, slippage=0.001)

    status, fill_price = portfolio.execute_order(10, 100)

    assert status == "FILLED"
    assert fill_price == pytest.approx(100.1)
    assert portfolio.position == 10
    assert portfolio.cash == 18999


def test_sell_with_slippage():

    portfolio = Portfolio(20000, transaction_cost=0.0, slippage=0.001)

    portfolio.execute_order(10, 100)

    status, fill_price = portfolio.execute_order(-10, 110)

    assert status == "FILLED"
    assert fill_price == pytest.approx(109.89)
    assert portfolio.position == 0
    assert portfolio.cash == 20097.9
