# External libraries
import numpy as np
from tinydb import Query

# Custom libraries
from . import database as db

### Nouveaux scoring
# 5 years average equity growth
def avg_equity_growth(ticker):
    df = db.statement(ticker, 'Balance Sheet', 'Annual')
    return df["Total stockholders' equity"].pct_change().tail(5).mean()

# 5 years average CROIC growth
def croic_growth(ticker):
    pass

# 5 years average operating cashflows growth
def avg_ocf_growth(ticker):
    df = db.statement(ticker, 'Cash Flow', 'Annual')
    return df['Net cash provided by operating activities'].pct_change().tail(5).mean()

# Payout ratio
def payout_ratio(ticker):
    pass

# Passif / equity
def liabilities_on_equity(ticker):
    pass

# Current ratio
def current_ratio(ticker):
    pass

# 5Y average IR coverage
def avg_ir_coverage(ticker):
    pass

# 5Y average dilution
def avg_dilution(ticker):
    pass

# 5Y average owners earnings
def owners_earnings(ticker):
    pass

# Utilisation du cash
def cash_user(ticker):
    pass

# Currency
def currency(db_name, ticker):
    return db.get(db_name).search(Query().ticker == ticker)[0]['currency']

# Average funds from operations
def average_ffops(db_name, ticker):
    ffo = np.array(db.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'funds_from_operations'))
    diluted_shares = np.array(db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'diluted_shares_outstanding'))
    return np.mean(np.divide(ffo, diluted_shares))

# Average funds from operations per share growth
def average_ffops_growth(db_name, ticker):
    return avg_growth_rate(db.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'funds_from_operations'))

# Average earnings per share
def average_eps(db_name, ticker):
    eps = np.array(db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'eps_diluted'))
    return np.mean(eps)

# Average earnings per share growth
def average_eps_growth(db_name, ticker):
    return avg_growth_rate(db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'eps_diluted'))


# Dilution
def average_dilution_rate(db_name, ticker):
    diluted_shares = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'diluted_shares_outstanding')
    return avg_growth_rate(diluted_shares)

# Payout ratio
def payout_ratio(db_name, ticker, dividend, date = None):
    d = db.latest_date(db_name, ticker, 'incomestatement', 'annual') if date == None else date
    ffo = db.get_value(db_name, ticker, 'cashflowstatement', 'annual', d, 'funds_from_operations')
    diluted_shares = db.get_value(db_name, ticker, 'incomestatement', 'annual', d, 'diluted_shares_outstanding')
    return (float(dividend) / (ffo / diluted_shares)) * 100

# Return on equity
def avg_roe(db_name, ticker):
    net_income = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'net_income')
    total_equity = db.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'total_equity')
    return np.mean(np.divide(net_income, total_equity)) * 100

# Return on invested capital
def avg_roic(db_name, ticker):
    net_income = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'net_income')
    total_equity = db.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'total_equity')
    long_term_debt = db.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'longterm_debt')
    return np.mean(np.divide(net_income, np.add(total_equity, long_term_debt))) * 100

# Cash return on invested capital
def avg_croic(db_name, ticker):
    free_cashflow = db.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'free_cash_flow')
    total_equity = db.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'total_equity')
    long_term_debt = db.get_historical_data(db_name, ticker, 'balancesheet', 'annual', 'longterm_debt')
    return np.mean(np.divide(free_cashflow, np.add(total_equity, long_term_debt))) * 100

# Free cash flows
def avg_fcf(db_name, ticker):
    free_cashflow = db.get_historical_data(db_name, ticker, 'cashflowstatement', 'annual', 'free_cash_flow')
    return np.mean(free_cashflow)

# Debt to market value
def debt_to_market_value(db_name, ticker, frequency, price, date = None):
    d = db.latest_date(db_name, ticker, 'incomestatement', frequency) if date == None else date
    capitalization = market_cap(db_name, ticker, frequency, price, d)
    debt = db.get_value(db_name, ticker, 'balancesheet', frequency, d, 'total_liabilities') * 1000000
    return (debt / capitalization) * 100

# Average growth rate
def avg_growth_rate(values):
    a = np.array(values).astype(float)
    return (np.nanmean(a[1:]/a[:-1]) - 1) * 100

# REITs EBITDA
def ebitda(db_name, ticker):
    net_income = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'net_income')
    total_interest_expense = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'total_interest_expense')
    tmp = np.add(net_income, total_interest_expense)
    income_taxes = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'income_taxes')
    tmp = np.add(tmp, income_taxes)
    depreciation_and_amortization = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'depreciation_and_amortization_expense')
    return np.add(tmp, depreciation_and_amortization)

# Stock EBITDA
def stock_ebitda(db_name, ticker):
    net_income = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'net_income')
    total_interest_expense = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'interest_expense')
    tmp = np.add(net_income, total_interest_expense)
    income_taxes = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'income_tax')
    tmp = np.add(tmp, income_taxes)
    depreciation_and_amortization = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'depreciation_and_amortization_expense')
    return np.add(tmp, depreciation_and_amortization)

# Average EBITDA
def avg_ebitda(db_name, ticker):
    return np.mean(ebitda(db_name, ticker))

# Average stock EBITDA
def avg_stock_ebitda(db_name, ticker):
    return np.mean(stock_ebitda(db_name, ticker))

# Average EBITDA growth rate
def avg_ebitda_growth(db_name, ticker):
    return avg_growth_rate(ebitda(db_name, ticker))

# Average stock EBITDA growth rate
def avg_stock_ebitda_growth(db_name, ticker):
    return avg_growth_rate(stock_ebitda(db_name, ticker))

# Average interest coverage
def avg_interest_coverage(db_name, ticker):
    interests = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'total_interest_expense')
    return np.mean(np.divide(ebitda(db_name, ticker), interests))

# Average interest coverage
def avg_stock_interest_coverage(db_name, ticker):
    interests = db.get_historical_data(db_name, ticker, 'incomestatement', 'annual', 'interest_expense')
    return np.mean(np.divide(stock_ebitda(db_name, ticker), interests))
