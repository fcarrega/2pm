import csv
from tinydb import TinyDB, Query

from . import shared

# Return given database name
def get(name):
    return TinyDB('db/' + name + '.json')

# Load a specific file
def read_financial_statement(ticker, statement, frequency):
    filename = 'data/' + ticker + '/' + ticker + statement + frequency + '.csv'
    data = {}
    with open(filename, newline = '') as csvfile:
        reader = csv.reader(csvfile)
        dates = next(reader, None)                      # Retrieve dates on file header
        for row in reader:                              # Loop on each line
            key = shared.parameterize(row[0].strip())   # Keep track of keys
            if not empty_row(row):                      # Only insert
                for index, value in enumerate(row[1:len(row)]):
                    date = shared.format_date(dates[index + 1])
                    shared.merge(data, data_to_insert(statement, frequency, date, key, value))
    return data


# Load Seeking Alpha financial statements files for a given ticker
def load_financial_statements(ticker):
    data = {}
    for statement in ['BalanceSheet', 'CashFlowStatement', 'IncomeStatement']:
        for frequency in ['Annual', 'Quarterly']:
            shared.merge(data, read_financial_statement(ticker, statement, frequency))
    return data

# Checks if a financial statement row is emtpy (title)
def empty_row(row):
    empty_row = False
    for element in row[1:len(row)-1]:
        if element == "":
            empty_row = empty_row or True
    return empty_row

def data_to_insert(statement, frequency, date, key, value):
    return {
        statement.lower(): {
            frequency.lower(): {
                date: {
                    key: shared.cast(value)
                }
            }
        }
    }
