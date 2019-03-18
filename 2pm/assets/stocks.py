# Standad library
import os
import sys

# External libraries
import click
from tinydb import Query
from money import Money

# Custom libraries
from . import shared
from . import database
from . import finance

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
@click.argument("stock")
def remove(stock):
    print("Removing stock " + stock + " from database...")
    Stock = Query()
    db.remove(Stock.ticker == stock)
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
def load_financial_statements():
    print("Updating financial statements for all stocks in DB...")
    stocks = db.all()
    for stock in stocks:
        print(stock['ticker'])
        database.load_financial_statements(stock['ticker'])

# Load financial statements for a unique stock
@stock.command()
@click.argument("stock")
def load_financial_statements_for(stock):
    print("Loading financial statements for {0}...".format(stock))
    financial_statements = database.load_financial_statements(stock)
    query = Query()
    db.update(financial_statements, query.ticker == stock)

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
@click.argument('price')
@click.argument('dividend')
def stats_for(ticker, price, dividend):
    print("Financial ratios for {0}:".format(ticker))
    currency = finance.currency('stocks', ticker)
    print("Market cap.|Yield|Debt-to-market value|Payout ratio|5Y avg. FFOPS|5Y avg. FFOPS growth rate|5Y avg. dil. rate|5Y avg. ROE|5Y avg. ROIC|5Y avg. CROIC|5Y avg. FCF")

    market_cap = finance.market_cap('stocks', ticker, 'quarterly', price) / 1000000
    current_yield = finance.current_yield(price, dividend)
    debt_to_market = finance.debt_to_market_value('stocks', ticker, 'quarterly', price)
    payout_ratio = finance.payout_ratio('stocks', ticker, dividend)
    avg_eps = finance.average_eps('stocks', ticker)
    avg_eps_growth = finance.average_eps_growth('stocks', ticker)
    avg_dil_rate = finance.average_dilution_rate('stocks', ticker)
    avg_roe = finance.avg_roe('stocks', ticker)
    avg_roic = finance.avg_roic('stocks', ticker)
    avg_croic = finance.avg_croic('stocks', ticker)
    avg_fcf = finance.avg_fcf('stocks', ticker)
    avg_ebitda = finance.avg_stock_ebitda('stocks', ticker)
    avg_ebitda_growth = finance.avg_stock_ebitda_growth('stocks', ticker)
    avg_interest_coverage = finance.avg_stock_interest_coverage('stocks', ticker)

    print("{0}|{1:.2f}%|{2:.2f}%|{3:.2f}%|{4}|{5:.2f}%|{6:.2f}%|{7:.2f}%|{8:.2f}%|{9:.2f}%|{10:.2f}|{11}|{12}|{13}".format(market_cap, current_yield, debt_to_market, payout_ratio, avg_eps, avg_eps_growth, avg_dil_rate, avg_roe, avg_roic, avg_croic, avg_fcf, avg_ebitda, avg_ebitda_growth, avg_interest_coverage))

    print("- Market capitalization: {0:.2f}".format(market_cap))
    print("- Yield: {0:.2f}%".format(current_yield))
    print("- Debt to market value: {0:.2f}%".format(debt_to_market))
    print("- Payout ratio: {0:.2f}%".format(payout_ratio))
    print("- 5Y avg. EPS: {0}".format(avg_eps))
    print("- 5Y avg. EPS growth rate: {0:.2f}%".format(avg_eps_growth))
    print("- 5Y avg. dilution rate: {0:.2f}%".format(avg_dil_rate))
    print("- 5Y avg. ROE: {0:.2f}%".format(avg_roe))
    print("- 5Y avg. ROIC: {0:.2f}%".format(avg_roic))
    print("- 5Y avg. CROIC: {0:.2f}%".format(avg_croic))
    print("- 5Y avg. FCF: {0:.2f}M {1}".format(avg_fcf, currency))
    print("- 5Y avg. EBITDA: {0:.2f}M {1}".format(avg_ebitda, currency))
    print("- 5Y avg. EBITDA growth rate: {0:.2f}%".format(avg_ebitda_growth))
    print("- 5Y avg. EBITDA interests coverage: {0:.2f}".format(avg_interest_coverage))
