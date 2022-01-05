"""Construct a simple Portfolio class that has a collection of Stocks and a "Profit" method that receives 2 dates and returns the profit of the
 Portfolio between those dates. Assume each Stock has a "Price" method that receives a date and returns its price.
Bonus Track: make the Profit method return the "annualized return" of the portfolio between the given dates."""
import yfinance
from datetime import datetime, timedelta
import json
from yahoo_fin import stock_info
import pandas as pd


class Portfolio:

    def __init__(self, id):
        self.id = id
        self.stocks_list = list()
    
    def profit(self, start_date, end_date):
        total_profit = 0
        for stock in self.stocks_list:
            price_start_date = stock.price(start_date)
            price_end_date = stock.price(end_date)
            valuation_start_date = price_start_date*stock.quantity
            valuation_end_date = price_end_date*stock.quantity
            total_profit += valuation_end_date - valuation_start_date
        return total_profit
    
    def get_annualized_return(self, start_date, end_date):
        profit = self.profit(start_date,end_date)
        annualized_return = profit
        return annualized_return

    def add_stock_to_portfolio(self, stock_object):
        self.stocks_list.append(stock_object)



class Stock:

    def __init__(self, id, symbol, quantity, initial_amount_invested_usd):
        self.id = id
        self.symbol = symbol
        self.quantity = quantity
        self.initial_amount_invested_usd = initial_amount_invested_usd
    
    def price(self, date):
        df = self.get_dataframe_ticker(date, date)
        price_at_date = df["Close"]
        return price_at_date
    
    def get_realtime_price(self):
        price = float(stock_info.get_live_price(self.symbol.lower()))
        return price
    
    def get_dataframe_ticker(self, start_date, end_date):
        ticker = yfinance.Ticker(self.symbol)
        df = ticker.history(interval="1d",start=start_date,end=end_date)
        return df


"""Ejecutable de ejemplo"""

if __name__ == '__main__':
    list_stocks_test = ['AMKR', 'AZPN', 'OZK', 'BBIO']
    id_portfolio = input("Enter the identification number for the new portfolio: ")
    portfolio_object = Portfolio(id_portfolio)
    index = 0
    for stock in list_stocks_test:
        money_invested_usd = float(input("Quantity of money in USD to invest in {}: ".format(stock)))
        price = float(stock_info.get_live_price(stock.lower()))
        #no se consideran comisiones
        quantity = money_invested_usd/price
        new_stock_object = Stock(index, stock, quantity, money_invested_usd)
        portfolio_object.add_stock_to_portfolio(new_stock_object)
        index += 1
    while True:
        start_date = input("Starting date to check the portfolio profits dd/mm/yy: ")
        end_date = input("Write a end date to check the portfolio profits dd/mm/yy: ")
        total_profit = portfolio_object.profit(start_date,end_date)
        print("Total profit: {} USD".format(total_profit))
        print("Annualized return: {} USD".format(total_profit))
    
