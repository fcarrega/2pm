# External libraries
import os
import sys
import click
from yahoo_finance import Share
from tinydb import Query

# Custom libraries
from . import shared
from . import database

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
        shared.output_string([reit['ticker'], reit['industry'], reit['currency'], reit['name']])

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
        database.load_financial_statements(reit['ticker'], 'reits')

# Load financial statements for a unique REIT
@reit.command()
@click.argument("reit")
def load_financial_statements_for(reit):
    print("Loading financial statements for {0}...".format(reit))
    financial_statements = database.load_financial_statements(reit)
    query = Query()
    db.update(financial_statements, query.ticker == reit)
