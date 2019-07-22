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
db = database.get('reits')

# Command group
@click.group()
def reit():
    pass

# Add REIT to database
@reit.command()
@click.argument("reit")
@click.argument("name")
@click.argument("reit_industry")
@click.argument("ccy")
def add(reit, name, reit_industry, ccy):
    print("Adding REIT " + reit + " (" + reit_industry + ")" " in database..." )
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

# Load financial statements for a unique REIT
@reit.command()
@click.argument("reit")
def load(reit):
    print("Loading financial statements for {0}...".format(reit))
    financial_statements = database.load_financial_statements(reit)

# Run financial analysis for a given REIT industry
@reit.command()
@click.argument('industry')
def run_analysis_for(industry):
    print("Running financial analysis for {0} REITs...".format(industry))
    reits = db.search(Query().industry == industry)
    tickers = []
    for reit in reits:
        tickers.append(reit['ticker'])
        # Yield
        # FFOPS growth rate
        # Dilution
        # ROE
        # CROIC


@reit.command()
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

@reit.command()
@click.argument('ticker')
def balance_sheet_for(ticker):
    print("Balance sheet for {0}:".format(ticker))
    print(database.statement(ticker, 'Balance Sheet', 'Annual').T)
    pass

@reit.command()
@click.argument('ticker')
def income_for(ticker):
    print("Income statement for {0}:".format(ticker))
    print(database.statement(ticker, 'Income Statement', 'Annual').T)
    pass

@reit.command()
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
