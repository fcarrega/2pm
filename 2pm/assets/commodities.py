# External libraries
import os
import sys
import click
from tinydb import Query

# Custom libraries
from .. import shared
from .. import database

# Initialize database connection
db = database.get('commodities')

# Group command
@click.group()
def commodity():
    pass

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
def add(cty, cty_class, ccy):
    print("Adding commodity " + cty + " (" + cty_class + ")" " in database..." )
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
