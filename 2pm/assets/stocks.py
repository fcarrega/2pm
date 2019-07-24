# Standad library
import os
import sys

# External libraries
import click
from tinydb import Query
from money import Money
import pandas

# Custom libraries
from .. import shared
from .. import database
from .. import finance

# Initialize database connection
db = database.get('stocks')

# Command group
@click.group()
def stock():
    pass

@stock.command()
@click.argument('ticker')
def price_for(ticker):
    print(finance.price(ticker))

# Get stocks prices
@stock.command()
def prices():
    stocks = db.all()
    for stock in stocks:
        get_stock_price(stock['ticker'], stock['industry'], stock['currency'])

# Add stock to database
@stock.command()
@click.argument("stock")
@click.argument("name")
@click.argument("stock_sector")
@click.argument("stock_industry")
@click.argument("ccy")
def add(stock, name, stock_sector, stock_industry, ccy):
    print("Adding stock " + stock + " (" + stock_sector + " / " + stock_industry + ")" " in database..." )
    db.insert({'ticker': stock, 'sector': stock_sector, 'industry': stock_industry, 'currency': ccy, 'name': name})
    print("Done !")

# Remove stock from database
@stock.command()
@click.argument("ticker")
def remove(stock):
    print("Removing stock " + ticker + " from database...")
    Stock = Query()
    db.remove(Stock.ticker == ticker)
    print("Done !")

# List available stocks
@stock.command()
def list():
    stocks = db.all()
    print("{0} Stocks in database :".format(len(stocks)))
    for stock in stocks:
        currency = '' if stock['currency'] == None else stock['currency']
        shared.output_string([stock['ticker'], stock['industry'], currency, stock['name']])

# List available stocks for a given industry
@stock.command()
@click.argument("industry")
def list_for(industry):
    query = Query()
    stocks = db.search(query.industry == industry)
    print("{0} {1} stocks in database :".format(len(stocks), industry))
    for stock in stocks:
        shared.output_string([stock['ticker'], stock['industry'], stock['currency'], stock['name']])

# Load stocks financial statements for all stocks in database
@stock.command()
@click.argument("ticker")
def load(ticker):
    print("Loading financial statements for {0}...".format(ticker))
    financial_statements = database.load_financial_statements(ticker)

# Load financial statements for a unique stock
@stock.command()
@click.argument("ticker")
def load_financial_statements_for(ticker):
    print("Loading financial statements for {0}...".format(ticker))
    financial_statements = database.load_financial_statements(ticker)
    query = Query()
    db.update(financial_statements, query.ticker == ticker)

# Run financial analysis for a given stock industry
@stock.command()
@click.argument('industry')
def run_analysis_for(industry):
    print("Running financial analysis for {0} stocks...".format(industry))
    stocks = db.search(Query().industry == industry)
    tickers = []
    for stock in stocks:
        tickers.append(stock['ticker'])
        # Yield
        # FFOPS growth rate
        # Dilution
        # ROE
        # CROIC

@stock.command()
@click.argument('ticker')
def stats_for(ticker):
    print("Financial ratios for {0}:".format(ticker))

    # Initialize stats
    statistics = pandas.DataFrame(stats(ticker))
    statistics.index = header()
    print(statistics)

    # Transpose matrix
    t = statistics.T.to_csv(index=False)
    print(t)

    pass


@stock.command()
@click.argument('ticker')
def balance_sheet_for(ticker):
    print("Balance sheet for {0}:".format(ticker))
    print(database.statement(ticker, 'Balance Sheet', 'Annual').T)
    pass

@stock.command()
@click.argument('ticker')
def income_for(ticker):
    print("Income statement for {0}:".format(ticker))
    print(database.statement(ticker, 'Income Statement', 'Annual').T)
    pass

@stock.command()
@click.argument('ticker')
def cashflow_for(ticker):
    print("Cash flow statement for {0}:".format(ticker))
    print(database.statement(ticker, 'Cash Flow', 'Annual').T)
    pass

def header():
    index = ('5Y avg. eq. growth',
             '5Y avg. CROIC growth',
             '5Y avg. OCF growth',
             'Payout ratio',
             'Liabilities / equity',
             'Current ratio',
             '5Y avg. IR coverage',
             '5Y avg. dilution',
             'Owners earnings',
             'Cash use')
    return index

def stats(ticker):
    statistics = [ finance.avg_equity_growth(ticker),     # 5Y average equity growth
                   finance.avg_croic_growth(ticker),      # 5Y average cash return on invested capital growth
                   finance.avg_ocf_growth(ticker),        # 5Y average operating cash flows growth
                   finance.payout_ratio(ticker),          # Payout ratio
                   finance.liabilities_on_equity(ticker), # Liabilities / equity
                   finance.current_ratio(ticker),         # Current ratio
                   finance.avg_ir_coverage(ticker),       # 5Y average IR coverage
                   finance.avg_dilution(ticker),          # 5Y average dilution
                   finance.owners_earnings(ticker),       # Owner's earnings
                   finance.cash_use(ticker) ]             # Cash use
    return statistics
