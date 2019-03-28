# Standad library
import os
import sys

# External libraries
import click
from tinydb import Query
from money import Money

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
@click.argument('price')
@click.argument('dividend')
def stats_for(ticker, price, dividend):
    print("Financial ratios for {0}:".format(ticker))
    currency = finance.currency('reits', ticker)
    print("Market cap.|Yield|Debt-to-market value|Payout ratio|5Y avg. FFOPS|5Y avg. FFOPS growth rate|5Y avg. dil. rate|5Y avg. ROE|5Y avg. ROIC|5Y avg. CROIC|5Y avg. FCF|5Y avg. EBITDA")

    market_cap = finance.market_cap('reits', ticker, 'quarterly', price) / 1000000
    current_yield = finance.current_yield(price, dividend)
    debt_to_market = finance.debt_to_market_value('reits', ticker, 'quarterly', price)
    payout_ratio = finance.payout_ratio('reits', ticker, dividend)
    avg_ffops = finance.average_ffops('reits', ticker)
    avg_ffops_growth = finance.average_ffops_growth('reits', ticker)
    avg_dil_rate = finance.average_dilution_rate('reits', ticker)
    avg_roe = finance.avg_roe('reits', ticker)
    avg_roic = finance.avg_roic('reits', ticker)
    avg_croic = finance.avg_croic('reits', ticker)
    avg_fcf = finance.avg_fcf('reits', ticker)
    avg_ebitda = finance.avg_ebitda('reits', ticker)
    avg_ebitda_growth = finance.avg_ebitda_growth('reits', ticker)
    avg_interest_coverage = finance.avg_interest_coverage('reits', ticker)

    print("{0}|{1:.2f}%|{2:.2f}%|{3:.2f}%|{4}|{5:.2f}%|{6:.2f}%|{7:.2f}%|{8:.2f}%|{9:.2f}%|{10:.2f}|{11}|{12:.2f}%|{13}".format(market_cap, current_yield, debt_to_market, payout_ratio, avg_ffops, avg_ffops_growth, avg_dil_rate, avg_roe, avg_roic, avg_croic, avg_fcf, avg_ebitda, avg_ebitda_growth, avg_interest_coverage))

    print("- Market capitalization: {0:.2f}".format(market_cap))
    print("- Yield: {0:.2f}%".format(current_yield))
    print("- Debt to market value: {0:.2f}%".format(debt_to_market))
    print("- Payout ratio: {0:.2f}%".format(payout_ratio))
    print("- 5Y avg. FFOPS: {0}".format(avg_ffops))
    print("- 5Y avg. FFOPS growth rate: {0:.2f}%".format(avg_ffops_growth))
    print("- 5Y avg. dilution rate: {0:.2f}%".format(avg_dil_rate))
    print("- 5Y avg. ROE: {0:.2f}%".format(avg_roe))
    print("- 5Y avg. ROIC: {0:.2f}%".format(avg_roic))
    print("- 5Y avg. CROIC: {0:.2f}%".format(avg_croic))
    print("- 5Y avg. FCF: {0:.2f}M {1}".format(avg_fcf, currency))
    print("- 5Y avg. EBITDA: {0:.2f}M {1}".format(avg_ebitda, currency))
    print("- 5Y avg. EBITDA growth rate: {0:.2f}%".format(avg_ebitda_growth))
    print("- 5Y avg. EBITDA interests coverage: {0:.2f}".format(avg_interest_coverage))

    # print("- Average PEG ratio")
    # print("- Reinvestment rate")
    # print("- Intrinsic value compounding rate")
