# External libraries
from numpy import mean
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
    return mean(database.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'funds_from_operations')) * 1000000

# Average AFFOPS

# Average adjusted funds from operations per share growth
def average_affops_growth(arg):
    pass

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
def dilution(ticker):
    pass

# Weighted average cost of capital
def wacc(ticker):
    pass

# Payout ratio
# EBITDA / coût de la dette
def payout_ratio(ticker):
    pass

# Return on equity
# Résultat net / capitaux propres
def roe(ticker):
    pass

# Return on investment
def roi(ticker):
    pass

# Return on invested capital
# Résultat net / (capitaux propres + dette LT)
def roic(ticker):
    pass

# Free cash flows
def fcf(ticker):
    pass

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
