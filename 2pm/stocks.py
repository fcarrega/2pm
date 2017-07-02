from yahoo_finance import Share
import csv

def get_quote(ticker):
    return (ticker, Share(ticker).get_price())


def get_quotes(ticker_list):
    for ticker in ticker_list:
        quote = get_quote(ticker)
        print(quote[0] + ',' + quote[1])


# Retail
# get_quotes(['FRT', 'GGP', 'KIM', 'MAC', 'O', 'REG', 'SLG', 'SPG', 'TCO'])

if __name__ == "__main__":
    # Diversified
    get_quotes([
                'ALX',
                'ALEX',
                'AAT',
                'AHH',
                'CLNS',
                'DS',
                'FREVS',
                # 'FCE.A',
                'GZT',
                'GOOD',
                'IRET',
                'LXP',
                'OLP',
                'PK',
                'HHC',
                'VER',
                'VNO',
                'WPC',
                'WRE'
              ])

#
# stocks = ['FRT', 'GGP', 'KIM', 'MAC', 'O', 'REG', 'SLG', 'SPG', 'TCO']
#
# for stock in stocks:
#     with open('data/' + stock + '/' + stock + 'BalanceSheetAnnual.csv', newline='') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
#         for row in spamreader:
#             line = ', '.join(row)
#             if line.startswith(" Total Debt"):
#                 print(stock + ',' + line)



    # get_price()
    # get_change()
    # get_percent_change()
    # get_volume()
    # get_prev_close()
    # get_open()
    # get_avg_daily_volume()
    # get_stock_exchange()
    # get_market_cap()
    # get_book_value()
    # get_ebitda()
    # get_dividend_share()
    # get_dividend_yield()
    # get_earnings_share()
    # get_days_high()
    # get_days_low()
    # get_year_high()
    # get_year_low()
    # get_50day_moving_avg()
    # get_200day_moving_avg()
    # get_price_earnings_ratio()
    # get_price_earnings_growth_ratio()
    # get_price_sales()
    # get_price_book()
    # get_short_ratio()
    # get_trade_datetime()
    # get_historical(start_date, end_date)
    # get_name()
    # refresh()
    # get_percent_change_from_year_high()
    # get_percent_change_from_year_low()
    # get_change_from_year_low()
    # get_change_from_year_high()
    # get_percent_change_from_200_day_moving_average()
    # get_change_from_200_day_moving_average()
    # get_percent_change_from_50_day_moving_average()
    # get_change_from_50_day_moving_average()
    # get_EPS_estimate_next_quarter()
    # get_EPS_estimate_next_year()
    # get_ex_dividend_date()
    # get_EPS_estimate_current_year()
    # get_price_EPS_estimate_next_year()
    # get_price_EPS_estimate_current_year()
    # get_one_yr_target_price()
    # get_change_percent_change()
    # get_dividend_pay_date()
    # get_currency()
    # get_last_trade_with_time()
    # get_days_range()
    # get_year_range()
