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
    currency = finance.currency('reits', ticker)
    header()
    stats(ticker)

    #
    # print("- Market capitalization: {0:.2f}".format(market_cap))
    # print("- Yield: {0:.2f}%".format(current_yield))
    # print("- Debt to market value: {0:.2f}%".format(debt_to_market))
    # print("- Payout ratio: {0:.2f}%".format(payout_ratio))
    # print("- 5Y avg. FFOPS: {0}".format(avg_ffops))
    # print("- 5Y avg. FFOPS growth rate: {0:.2f}%".format(avg_ffops_growth))
    # print("- 5Y avg. dilution rate: {0:.2f}%".format(avg_dil_rate))
    # print("- 5Y avg. ROE: {0:.2f}%".format(avg_roe))
    # print("- 5Y avg. ROIC: {0:.2f}%".format(avg_roic))
    # print("- 5Y avg. CROIC: {0:.2f}%".format(avg_croic))
    # print("- 5Y avg. FCF: {0:.2f}M {1}".format(avg_fcf, currency))
    # print("- 5Y avg. EBITDA: {0:.2f}M {1}".format(avg_ebitda, currency))
    # print("- 5Y avg. EBITDA growth rate: {0:.2f}%".format(avg_ebitda_growth))
    # print("- 5Y avg. EBITDA interests coverage: {0:.2f}".format(avg_interest_coverage))

def header():
    h = ('5Y avg. CROIC growth,'
         '5Y avg. OCF growth,'
         '5Y avg. eq. growth,'
         'Payout ratio,'
         'Liab. / eq.,'
         'Current ratio,'
         '5Y avg. IR cov.,'
         '5Y avg. dilution,'
         'Owners earnings,'
         'Cash use')
    print(h)

def stats(ticker):
    # 5Y average cash return on invested capital growth
    print('{0:.2f}%'.format(finance.avg_croic_growth(ticker)))

    # 5Y average operating cash flows growth
    print('{0:.2f}%'.format(finance.avg_ocf_growth(ticker)))

    # 5Y average equity growth
    print('{0:.2f}%'.format(finance.avg_equity_growth(ticker)))

    # Payout ratio
    print(finance.payout_ratio(ticker))

    # Liabilities / equity
    print(finance.liabilities_on_equity(ticker))

    # Current ratio
    print(finance.current_ratio(ticker))

    # 5Y average IR coverage
    print('{0:.2f}%'.format(finance.avg_ir_coverage(ticker)))

    # 5Y average dilution
    print('{0:.2f}%'.format(finance.avg_dilution(ticker)))

    # Owner's earnings
    print(finance.owners_earnings(ticker))

    # Cash use
    print(finance.cash_use(ticker))
