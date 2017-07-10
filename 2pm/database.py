import csv
from tinydb import TinyDB


def get(name):
    return TinyDB('db/' + name + '.json')

# Load a specific file
def load_financial_statement(ticker, statement, frequency):
    filename = 'data/' + ticker + '/' + ticker + statement + frequency + '.csv'
    with open(filename, newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            print(', '.join(row))

# Load Seeking Alpha financial statements files for a given ticker
def load_financial_statements(ticker):
    for statement in ['BalanceSheet', 'CashFlowStatement', 'IncomeStatement']:
        for frequency in ['Annual', 'Quarterly']:
            load_financial_statement(ticker, type, statement, frequency)
