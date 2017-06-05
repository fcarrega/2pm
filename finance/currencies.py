# External libraries
import os
import sys
from yahoo_finance import Currency
from tinydb import Query

# Custom libraries
import shared
import database

# Retrieve a given FX Rate
def get_fx_rate(ccy):
    fx = Currency(ccy + 'EUR')
    rate = fx.get_rate()
    timestamp = fx.get_trade_datetime()
    shared.output_string([ccy, 'EUR', rate, timestamp])

def get_fx_rates(db):
    currencies = db.all()
    for currency in currencies:
        get_fx_rate(currency['iso'])

def add(ccy, db):
    print("Adding currency " + ccy + " in database..." )
    db.insert({'iso': ccy})
    print("Done !")

def remove(ccy, db):
    print("Removing currency " + ccy + " from database...")
    Ccy = Query()
    db.remove(Ccy.iso == ccy)
    print("Done !")

def list(db):
    print("Available currencies :")
    currencies = db.all()
    for currency in currencies:
        print(currency['iso'])

if __name__ == "__main__":
    db = database.get('currencies')
    action = sys.argv[1]
    if action == 'add':
        add(sys.argv[2], db)
    elif action == 'remove':
        remove(sys.argv[2], db)
    elif action == 'list':
        list(db)
    elif action == 'get_rates':
        get_fx_rates(db)
    else:
        print("Action not recognized. Correct actions : add, remove, list, get_rates")
