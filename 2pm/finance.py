from tinydb import Query

from . import database

# ROI
# ROIC
# CROIC

# Current market capitalization
def market_cap(db_name, ticker, frequency, date = None):
    d = database.latest_date(db_name, ticker, 'incomestatement', frequency) if date == None else date
    nb_shares = database.get_value(db_name, ticker, 'incomestatement', frequency, d, 'diluted_shares_outstanding') * 1000000
    price = 158.00
    return nb_shares * price

# Loan-to-value
def loan_to_value(ticker):
    pass

# Average adjusted funds from operations per share
def average_affops(ticker):
    pass

# Average adjusted funds from operations per share growth
def average_affops_growth(arg):
    pass

# Current yield
def current_yield(ticker):
    pass

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
