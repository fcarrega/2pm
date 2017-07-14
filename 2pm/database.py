import csv
from tinydb import TinyDB

# Return given database name
def get(name):
    return TinyDB('db/' + name + '.json')

# Load a specific file
def load_financial_statement(ticker, statement, frequency):
    filename = 'data/' + ticker + '/' + ticker + statement + frequency + '.csv'
    with open(filename, newline = '') as csvfile:
        reader = csv.reader(csvfile)
        dates = next(reader, None)                  # Retrieve dates on file header
        for row in reader:                          # Loop on each line
            key = row[0].strip()                    # Keep track of keys
            if not empty_row(row):                  # Only insert
                for index, value in enumerate(row[1:len(row)-1]):
                    string_to_output = key + ": "
                    string_to_output += dates[index] + ': '
                    string_to_output += value + ' | '
                    print(string_to_output)

# Load Seeking Alpha financial statements files for a given ticker
def load_financial_statements(ticker):
    for statement in ['BalanceSheet', 'CashFlowStatement', 'IncomeStatement']:
        for frequency in ['Annual', 'Quarterly']:
            load_financial_statement(ticker, statement, frequency)

# Checks if a financial statement row is emtpy (title)
def empty_row(row):
    empty_row = False
    for element in row[1:len(row)-1]:
        if element == "":
            empty_row = empty_row or True
    return empty_row
