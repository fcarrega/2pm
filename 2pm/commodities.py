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
db = database.get('commodities')

# Group command
@click.group()
def commodity():
    pass

# Retrieve a given FX Rate
def get_price(ticker, cty_class, ccy):
    commodity = Share(ticker)
    price = commodity.get_price()
    datetime = commodity.get_trade_datetime()
    shared.output_string([cty_class, ticker, price, ccy, datetime])

# Retrieve commodities prices
@commodity.command()
def get_prices():
    commodities = db.all()
    for commodity in commodities:
        get_price(commodity['ticker'], commodity['class'], commodity['currency'])

# Add commodity to database
@commodity.command()
@click.argument('cty')
@click.argument('cty_class')
def add(cty, cty_class):
    print("Adding commodity " + cty + " (" + cty_class + ")" " in database..." )
    ccy = Share(cty).get_currency()
    db.insert({'ticker': cty, 'class': cty_class, 'currency': ccy})
    print("Done !")

# Remove commodity from database
@commodity.command()
@click.argument('cty')
def remove(cty):
    print("Removing commodity " + cty + " from database...")
    Cty = Query()
    db.remove(Cty.ticker == cty)
    print("Done !")

# List available commodities in database
@commodity.command()
def list():
    print("Available commodities :")
    commodities = db.all()
    for commodity in commodities:
        shared.output_string([commodity['ticker'], commodity['class'], commodity['currency']])
