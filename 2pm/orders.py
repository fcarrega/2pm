# External libraries
import os
import sys
from yahoo_finance import Currency
from tinydb import Query

# Custom libraries
from . import shared
from . import database

def new(date, ticker, way, quantity, price, db):
    print("Adding order in database..." )
    db.insert({'date': date, 'ticker': ticker, 'way': way, 'quantity': quantity, 'price': price})
    print("Done !")
