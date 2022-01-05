"""Construct a simple Portfolio class that has a collection of Stocks and a "Profit" method that receives 2 dates and returns the profit of the
 Portfolio between those dates. Assume each Stock has a "Price" method that receives a date and returns its price.
Bonus Track: make the Profit method return the "annualized return" of the portfolio between the given dates."""

import yfinance
from datetime import datetime, timedelta
import json
from yahoo_fin import stock_info


class Portfolio:


    def __init__(self, id):
        """Each portfolio has a unique id which is needed to initialize it"""
        self.id = id
        self.stocks_list = list()
    
    def profit(self, start_date, end_date):
        total_profit = 0
        for stock in self.stocks_list:
            price_start_date = stock.price(start_date)
            price_end_date = stock.price(end_date)
            money_invested = stock.initial_amount_invested_usd 
            quantity = money_invested/price_start_date
            valuation_end_date = price_end_date*quantity
            total_profit += valuation_end_date - money_invested
        return total_profit
    
    def get_annualized_return(self, start_date, end_date):
        profit = self.profit(start_date,end_date)
        annualized_return = profit
        return annualized_return

    def add_stock_to_portfolio(self, stock_object):
        self.stocks_list.append(stock_object)



class Stock:


    def __init__(self, id, symbol, initial_amount_invested_usd):
        """Each stock object is initialized by a unique id, the symbol of the stock, the quantity of the stock on the position and the intial
         investment in USD"""
        self.id = id
        self.symbol = symbol
        self.initial_amount_invested_usd = initial_amount_invested_usd
    
    def price(self, date):
        """So as to get the dataframe of the prices for stock on a specific date, the next days date is calculated 
        and then the first row of the dataframe has the price data of the stock on the specified date.
        
        In this specific case i chose to get the closing price of the stock on that specific date as the reference price for profit calculations.
        """
        end_date = self.get_next_day_date(date)
        df = self.get_dataframe_ticker(date, end_date)
        price_at_date = df["Close"][0]
        return price_at_date
    
    def get_dataframe_ticker(self, start_date, end_date):
        ticker = yfinance.Ticker(self.symbol)
        df = ticker.history(interval="1d",start=start_date,end=end_date)
        return df
    
    def get_next_day_date(self, initial_date):
        datetime_object_initial_date = datetime.strptime(initial_date, '%Y-%m-%d')
        next_day_delta = timedelta(days = 1)
        end_date = str(datetime_object_initial_date + next_day_delta).split(" ")[0]
        return end_date


"""Runnable example"""
if __name__ == '__main__':
    # Edit the stock list as you please
    list_stocks_test = ['TSLA', 'AMZN', 'ROKU', 'PFE']
    id_portfolio = input("\n Enter the identification number for the new portfolio: ")
    # New portfolio object is created
    portfolio_object = Portfolio(id_portfolio)
    index = 0
    total_money_invested = 0
    # For each stock in the initial list of stocks we create a new Stock object and add it to the list of stocks in the Portfolio object
    for stock_symbol in list_stocks_test:
        money_invested_usd = float(input("\n Quantity of money in USD to invest in {}: ".format(stock_symbol)))
        """ In this example """
        new_stock_object = Stock(index, stock_symbol, money_invested_usd)
        portfolio_object.add_stock_to_portfolio(new_stock_object)
        total_money_invested += money_invested_usd
    while True:
        start_date = input("\nEnter a starting date to check the portfolio profits yy-mm-dd: ")
        end_date = input("Enter an end date to check the portfolio profits yy-mm-yy: ")
        total_profit = portfolio_object.profit(start_date,end_date)
        print("\nSummary of portfolio performance between {} and {}: \n".format(start_date, end_date))
        print(" Total initial investment: {} USD".format(total_money_invested))
        print(" Total profit: {} USD".format(total_profit))
        print(" Annualized return: {} USD".format(total_profit))
    
