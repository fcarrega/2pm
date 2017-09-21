# External libraries
import numpy as np
from yahoo_finance import Share
from tinydb import Query

# Custom libraries
from . import database

# ROI
# ROIC
# CROIC

# Current price
def price(ticker):
    return Share(ticker).get_price()

# Currency
def currency(db_name, ticker):
    return database.get(db_name).search(Query().ticker == ticker)[0]['currency']

# Current market capitalization
def market_cap(db_name, ticker, frequency, date = None):
    d = database.latest_date(db_name, ticker, 'incomestatement', frequency) if date == None else date
    nb_shares = database.get_value(db_name, ticker, 'incomestatement', frequency, d, 'diluted_shares_outstanding') * 1000000
    return nb_shares * float(price(ticker))

# Loan-to-value
def loan_to_value(ticker):
    pass

# Average funds from operations
def average_ffops(db_name, ticker):
    ffo = np.array(database.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'funds_from_operations'))
    diluted_shares = np.array(database.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'diluted_shares_outstanding'))
    return np.mean(np.divide(ffo, diluted_shares))

# Average funds from operations per share growth
def average_ffops_growth(db_name, ticker):
    return avg_growth_rate(database.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'funds_from_operations'))

# Current yield
def current_yield(ticker):
    return Share(ticker).get_dividend_yield()

# Yield on cost
def yield_on_cost(ticker):
    pass

# Beta
def beta(ticker):
    pass

# Dilution
def average_dilution_rate(db_name, ticker):
    diluted_shares = database.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'diluted_shares_outstanding')
    return avg_growth_rate(diluted_shares)

# Weighted average cost of capital
def wacc(ticker):
    pass

# Payout ratio
# EBITDA / coût de la dette
def payout_ratio(ticker):
    pass

# Return on equity
def avg_roe(db_name, ticker):
    net_income = database.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'net_income')
    total_equity = database.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'total_equity')
    return np.mean(np.divide(net_income, total_equity)) * 100

# Return on investment
def roi(ticker):
    pass

# Return on invested capital
def avg_roic(db_name, ticker):
    net_income = database.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'net_income')
    total_equity = database.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'total_equity')
    long_term_debt = database.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'longterm_debt')
    return np.mean(np.divide(net_income, np.add(total_equity, long_term_debt))) * 100

# Cash return on invested capital
def avg_croic(db_name, ticker):
    free_cashflow = database.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'free_cash_flow')
    total_equity = database.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'total_equity')
    long_term_debt = database.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'longterm_debt')
    return np.mean(np.divide(free_cashflow, np.add(total_equity, long_term_debt))) * 100


# Free cash flows
def avg_fcf(db_name, ticker):
    free_cashflow = database.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'free_cash_flow')
    return np.mean(free_cashflow)

# Average PEG
def average_peg(ticker):
    pass

# Reinvestment rate (RR)
# Invested incremental capital / total earnings
def reinvestment_rate(ticker):
    pass

# Intrinsic value compounding rate
# ROIC x RR
def ivcr(ticker):
    pass

# Average growth rate
def avg_growth_rate(values):
    a = np.array(values).astype(float)
    return (np.nanmean(a[1:]/a[:-1]) - 1) * 100

def discounted_cashflow_value(arg):
    pass

def divident_discount_value(arg):
    pass
