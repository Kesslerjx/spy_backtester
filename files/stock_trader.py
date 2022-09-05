
# Loops through each day, but makes a trade every n_days 
from math import copysign, floor
from multiprocessing import resource_tracker
from typing import Dict
from xmlrpc.client import Boolean

# Determines the amount of stocks to buy
# Will return 0 if certain conditions aren't met
def get_amount_to_buy(balance: float, cost: float, buy_max: Boolean, buy_amount: int or None) -> int:
    if buy_max:
        return int(floor(balance / cost))
    elif not(buy_amount == None) and buy_amount > 0:
        return buy_amount
    else:
        return 0

# Will trade stocks only
# If the previous day was red, it will buy at the close price and sell the n_day at the close price
# If the previous day was green, it will short the stock - sell at the open price, buy and sell at close price, take the difference
# It assumes you are checking the market the day prior
def trade_ndays(days: list, start_balance: float, n_days: int, buy_max: Boolean = True, buy_amount: int = None):

    balance = start_balance

    for index, day in enumerate(days):
        if index % n_days == 0 and not(index == 0):
            prev_candle = days[index-1].close - days[index-1].open  # Get the previous days change amount
            prev_candle = copysign(1, prev_candle) # Get the sign to determine direction

            # Gets the buy price based on the direction of the previous candle
            if prev_candle > 0:
                buy_price = day.open
                to_buy    = get_amount_to_buy(balance, buy_price, buy_max, buy_amount)
                value     = buy_price * to_buy # Value of the loaned stocks
                balance   = balance + value # You sell the loaned stocks
                eod       = day.close * to_buy # Value of the stock at the end of the day
                balance   = balance - eod # You buy the stock at the eod value
            else:
                buy_price = days[index-1].close
                to_buy    = get_amount_to_buy(balance, buy_price, buy_max, buy_amount)
                cost      = buy_price * to_buy
                balance   = balance - cost # Update the balance - stocks have been purchased
                eod       = day.close * to_buy # Get the value of the stocks at the end of the day
                balance   = balance + eod # Update the balance - stocks have been sold

    percent_change = round((balance - start_balance) / start_balance, 2)

    results = dict()

    results['Start Balance']  = start_balance
    results['End Balance']    = balance
    results['Percent Change'] = percent_change
    results['N Days']         = n_days

    return results

# Returns the results that have the largest end balance
def get_best_trade_results(days: list, start_balance: float, buy_max: Boolean = True, buy_amount: int = None, times: int = 30):
    
    results = None

    for n in range(1, times, 1):
        r = trade_ndays(days, start_balance, n, buy_max, buy_amount)

        if results == None or r['End Balance'] > results['End Balance']:
            results = r

    return results
