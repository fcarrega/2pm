# Standad library
import os
import sys

# External libraries
import click
from yahoo_finance import Share
from tinydb import Query
from money import Money

# Custom libraries
from . import shared
from . import database
from . import finance

# Initialize database connection
db = database.get('reits')

# Command group
@click.group()
def reit():
    pass

# Retrieve REIT price
def get_reit_price(ticker, reit_industry, ccy):
    reit = Share(ticker)
    price = reit.get_price()
    datetime = reit.get_trade_datetime()
    shared.output_string([reit_industry, ticker, price, ccy, datetime])

@reit.command()
@click.argument('ticker')
def price_for(ticker):
    print(finance.price(ticker))

# Get REITs prices
@reit.command()
def prices():
    reits = db.all()
    for reit in reits:
        get_reit_price(reit['ticker'], reit['industry'], reit['currency'])

# Add REIT to database
@reit.command()
@click.argument("reit")
@click.argument("name")
@click.argument("reit_industry")
def add(reit, name, reit_industry):
    print("Adding REIT " + reit + " (" + reit_industry + ")" " in database..." )
    ccy = Share(reit).get_currency()
    db.insert({'ticker': reit, 'sector': 'REIT', 'industry': reit_industry, 'currency': ccy, 'name': name})
    print("Done !")

# Remove REIT from database
@reit.command()
@click.argument("reit")
def remove(reit):
    print("Removing REIT " + reit + " from database...")
    Reit = Query()
    db.remove(Reit.ticker == reit)
    print("Done !")

# List available REITs
@reit.command()
def list():
    reits = db.all()
    print("{0} REITS in database :".format(len(reits)))
    for reit in reits:
        currency = '' if reit['currency'] == None else reit['currency']
        shared.output_string([reit['ticker'], reit['industry'], currency, reit['name']])

# List available REITs for a given industry
@reit.command()
@click.argument("industry")
def list_for(industry):
    query = Query()
    reits = db.search(query.industry == industry)
    print("{0} {1} REITS in database :".format(len(reits), industry))
    for reit in reits:
        shared.output_string([reit['ticker'], reit['industry'], reit['currency'], reit['name']])

# Load REITS financial statements for all REITs in database
@reit.command()
def load_financial_statements():
    print("Updating financial statements for all REITs in DB...")
    reits = db.all()
    for reit in reits:
        print(reit['ticker'])
        database.load_financial_statements(reit['ticker'])

# Load financial statements for a unique REIT
@reit.command()
@click.argument("reit")
def load_financial_statements_for(reit):
    print("Loading financial statements for {0}...".format(reit))
    financial_statements = database.load_financial_statements(reit)
    query = Query()
    db.update(financial_statements, query.ticker == reit)

# Run financial analysis for a given REIT industry
@reit.command()
@click.argument('industry')
def run_analysis_for(industry):
    print("Running financial analysis for {0} REITs...".format(industry))

@reit.command()
@click.argument('ticker')
def stats_for(ticker):
    print("Financial ratios for {0}:".format(ticker))
    currency = finance.currency('reits', ticker)
    print("- Market capitalization: {0}".format(str(Money(finance.market_cap('reits', ticker, 'quarterly'), currency))))
    print("- Yield: {0}%".format(finance.current_yield(ticker)))
    # print("- Yield on cost:")
    print("- 5Y avg. FFOPS: {0}".format(str(Money(finance.average_ffops('reits', ticker), currency))))
    print("- 5Y avg. FFOPS growth rate: {0:.2f}%".format(finance.average_ffops_growth('reits', ticker)))
    print("- 5Y avg. dilution rate: {0:.2f}%".format(finance.average_dilution_rate('reits', ticker)))
    print("- 5Y avg. ROE: {0:.2f}%".format(finance.avg_roe('reits', ticker)))
    print("- 5Y avg. ROIC: {0:.2f}%".format(finance.avg_roic('reits', ticker)))
    print("- 5Y avg. CROIC: {0:.2f}%".format(finance.avg_croic('reits', ticker)))
    print("- 5Y avg. FCF: {0:.2f}M {1}".format(finance.avg_fcf('reits', ticker), currency))
    # print("- Beta:")
    # print("- Weighted average cost of capital (WACC):")
    print("- Payout ratio:")
    print("- Average PEG ratio")
    print("- Reinvestment rate")
    print("- Intrinsic value compounding rate")
    print("- Discounted cashflow value (DCF model)")
    print("- Dividend Discount value (DCM model)")
