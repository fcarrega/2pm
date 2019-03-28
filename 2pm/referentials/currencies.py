# External libraries
import os
import sys
import click
from tinydb import Query

# Custom libraries
from .. import shared
from .. import database

# Initialize database connection
db = database.get('currencies')

# Group command
@click.group()
def currency():
    pass

# Retrieve a given FX Rate - standalone method
def get_fx_rate(ccy):
    fx = Currency(ccy + 'EUR')
    rate = fx.get_rate()
    timestamp = fx.get_trade_datetime()
    shared.output_string([ccy, 'EUR', rate, timestamp])

# Retrieve & display FX rates
@currency.command()
def fx_rates():
    currencies = db.all()
    for currency in currencies:
        get_fx_rate(currency['iso'])

# Add currency to database
@currency.command()
@click.argument('ccy')
def add(ccy):
    print("Adding currency " + ccy + " in database..." )
    db.insert({'iso': ccy})
    print("Done !")

# Remove currency from database
@currency.command()
@click.argument('ccy')
def remove(ccy):
    print("Removing currency " + ccy + " from database...")
    Ccy = Query()
    db.remove(Ccy.iso == ccy)
    print("Done !")

# List all available currencies in database
@currency.command()
def list():
    print("Available currencies :")
    currencies = db.all()
    for currency in currencies:
        print(currency['iso'])
