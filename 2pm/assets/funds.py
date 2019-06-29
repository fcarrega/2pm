# External libraries
import os
import sys
import click
from tinydb import Query

# Custom libraries
from .. import shared
from .. import database

# Initialize database connection
db = database.get('mutual_funds')

# Group command
@click.group()
def fund():
    pass

# Add mutual fund to database
@fund.command()
@click.argument("fund")
@click.argument("fund_class")
@click.argument("fund_subclass")
@click.argument("ccy")
def add(fund, fund_class, fund_subclass, ccy):
    print("Adding mutual fund " + fund + " (" + fund_class + "/" + fund_subclass + ")" " in database..." )
    db.insert({'ticker': fund, 'sector': 'Mutual fund', 'class': fund_class, 'subclass': fund_subclass, 'currency': ccy})
    print("Done !")

# Remove mutual fund
@fund.command()
@click.argument("fund")
def remove(fund):
    print("Removing fund " + fund + " from database...")
    Fund = Query()
    db.remove(Fund.ticker == fund)
    print("Done !")

# List available mutual funds
@fund.command()
def list():
    print("Available Mutual funds :")
    funds = db.all()
    for fund in funds:
        shared.output_string([fund['ticker'], fund['class'], fund['subclass'], fund['currency']])
