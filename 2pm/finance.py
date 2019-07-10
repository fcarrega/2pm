# External libraries
import numpy as np
from tinydb import Query

# Custom libraries
from . import database as db

# 5 years average equity growth
def avg_equity_growth(ticker):
    df = db.statement(ticker, 'Balance Sheet', 'Annual')
    return df["Total stockholders' equity"].pct_change().tail(5).mean()

# 5 years average CROIC growth
def avg_croic_growth(ticker):
    fcf = db.statement(ticker, 'Cash flow', 'Annual')['Free cash flow']
    equity = db.statement(ticker, 'Balance sheet', 'Annual')["Total stockholders' equity"]
    lt_debt = db.statement(ticker, 'Balance sheet', 'Annual')['Long-term debt']
    croic = fcf / (equity + lt_debt)
    return croic.pct_change().tail(5).mean()

# 5 years average operating cashflows growth
def avg_ocf_growth(ticker):
    df = db.statement(ticker, 'Cash Flow', 'Annual')
    return df['Net cash provided by operating activities'].pct_change().tail(5).mean()

# Payout ratio
def payout_ratio(ticker):
    dividend = db.statement(ticker, 'Cash flow', 'Annual')['Cash dividends paid']
    net_income = db.statement(ticker, 'Income statement', 'Annual')['Net income']
    ratio = - dividend / net_income
    return ratio.iloc[-1]

# Passif / equity
def liabilities_on_equity(ticker):
    df = db.statement(ticker, 'Balance sheet', 'Quarterly')
    liabilities = df['Total liabilities'].tail(1)
    equity = df["Total stockholders' equity"].tail(1)
    ratio = liabilities / equity
    return ratio.iloc[-1] * -1

# Current ratio
def current_ratio(ticker):
    df = db.statement(ticker, 'Balance sheet', 'Quarterly').iloc[-1]
    assets = df['Cash and cash equivalents'] + df['Receivables']
    liabilities = df['Payables and accrued expenses']
    return assets / liabilities

# 5Y average IR coverage
def avg_ir_coverage(ticker):
    income_statement = db.statement(ticker, 'Income statement', 'Annual')
    ebitda = income_statement['EBITDA']
    depreciation_and_amortization = income_statement['Depreciation and amortization']
    interest_expense = income_statement['Interest expenses']
    coverage = (ebitda - depreciation_and_amortization) / interest_expense
    return coverage.tail(5).mean()

# 5Y average dilution
def avg_dilution(ticker):
    df = db.statement(ticker, 'Income statement', 'Annual')
    # Manage duplicated column names (EPS & shares outstanding)
    return df['Diluted'].iloc[:,-1].pct_change().tail(5).mean()

# 5Y average owners earnings
def owners_earnings(ticker):
    cashflows = db.statement(ticker, 'Cash flow', 'Annual')
    fcf = cashflows['Free cash flow']
    capex = cashflows['Other investing activities']
    owners_earnings = (fcf - capex) / fcf
    return owners_earnings.tail(5).mean()

# Utilisation du cash
def cash_use(ticker):
    equity = db.statement(ticker, 'Balance sheet', 'Annual')["Total stockholders' equity"]
    delta_equity = equity.iloc[-1] - equity[0]

    dividend = db.statement(ticker, 'Cash flow', 'Annual')['Cash dividends paid']
    paid_dividends = dividend.sum() * -1

    net_income = db.statement(ticker, 'Income statement', 'Annual')['Net income']
    total_net_income = net_income.sum()

    return (delta_equity + paid_dividends) / total_net_income

# Currency
def currency(db_name, ticker):
    return db.get(db_name).search(Query().ticker == ticker)[0]['currency']
