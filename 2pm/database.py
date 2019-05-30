import os
import csv
import pandas
from pathlib import Path
from tinydb import TinyDB, Query

from . import shared

# Return given database name
def get(name):
    return TinyDB('db/' + name + '.json')

# Load a specific file
def read_financial_statement(ticker, statement, frequency):
    name = filename(ticker, statement, frequency)
    source = pandas.read_csv(name, delimiter = ',', header = 1)

    # Transpose matrix to use time series
    source = source.T

    # Use first line as column names
    source.columns = source.iloc[0]

    # Remove first line to keep only data
    source = source.iloc[1:]

    # Remove last line if TTM
    if 'TTM' in source.index:
        source = source.drop('TTM')

    dir = pickle_dir(ticker)
    file = pickle_file(ticker, statement, frequency)
    if Path(dir).is_dir():
        if Path(dir + file).is_file():
            existing = pandas.read_pickle(dir + file)
            existing.merge(source)
        source.to_pickle(dir + file)
    else:
        os.mkdir(dir)
    return

# Load Morningstar financial statements files for a given ticker
def load_financial_statements(ticker):
    data = {}
    for statement in ['Balance Sheet', 'Cash Flow', 'Income Statement']:
        for frequency in ['Annual', 'Quarterly']:
            read_financial_statement(ticker, statement, frequency)
    return data

# Latest date available for a given ticker, financial statement and frequency
def latest_date(db_name, ticker, statement, frequency):
    dates = available_dates(db_name, ticker, statement, frequency)
    return str(max(list(map(int, dates))))

# Available dates for a given ticker, statement and frequency
def available_dates(db_name, ticker, statement, frequency):
    db = get(db_name)
    q = Query()
    return list(db.search(q.ticker == ticker)[0][statement][frequency].keys())

# Retrieve specific value in DB
def get_value(db_name, ticker, statement, frequency, date, entry):
    return get(db_name).search(Query().ticker == ticker)[0][statement][frequency][date][entry]

# Returns a list of historical data
def get_historical_data(db_name, ticker, statement, frequency, entry):
    data = get(db_name).search(Query().ticker == ticker)[0][statement][frequency]
    result = []
    for k in sorted(data):
        result.append(data[k][entry])
    return result

def filename(ticker, statement, frequency):
    return './data/' + ticker + '/' + ticker + ' ' + statement + ' ' + frequency + '.csv'

def pickle_dir(ticker):
    return 'data/frames/' + ticker + '/'

def pickle_file(ticker, statement, frequency):
    return ticker + ' ' + statement + ' ' + frequency + '.pkl'
#
# ticker = 'MAC'
# statement = 'Balance Sheet'
# statement = 'Cash Flow'
# frequency = 'Annual'
# dir = pickle_dir(ticker)
# file = pickle_file(ticker, statement, frequency)
# df = pandas.read_pickle(dir + file)
# df
