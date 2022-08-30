import statistics
import holidays
import numpy as np
from math import copysign, floor
from csv_reader import get_days
from datetime import datetime, timedelta

# --- CONSTANTS --- #
# Get the days from the CSV file
# Get holidays for forecasting purposes
DAYS     = get_days('./data/spy_daily_since_2021.csv')
HOLIDAYS = holidays.US()

S_BALANCE_DEFAULT = 1000
C_COST_DEFAULT    = 400
DELTA_DEFAULT     = 0.50

# --- FUNCTIONS --- #
# Returns true if a swing
# Returns false if not
def is_swing(day, next_day):

    day_difference  = day.close - day.open
    next_difference = next_day.close - next_day.open

    return not(copysign(1, day_difference) == copysign(1, next_difference))

def add_day(date: str, days=1):
    date_as_date = datetime.strptime(date, '%Y-%m-%d')
    days_delta   = timedelta(days)
    new_date     = date_as_date + days_delta
    date_string  = new_date.strftime('%Y-%m-%d')
    return date_string

def is_weekend(date: str):
    date_as_date = datetime.strptime(date, '%Y-%m-%d')
    if date_as_date.weekday() <= 4:
        return False
    else:
        return True

def is_holiday(date: str):
    return date in HOLIDAYS

def is_business_day(date: str):
    return not(is_holiday(date)) and not(is_weekend(date))

def get_forecast(start_date, amount, days):
    forecast = []
    f_count = 1
    d_count = 1

    while f_count <= amount:

        while d_count <= days:
            # Add a day
            start_date = add_day(start_date)
            # Only count the day if it's a business day
            if is_business_day(start_date):
                d_count = d_count + 1

        forecast.append(start_date)
        d_count = 1
        f_count = f_count + 1 

    return forecast

def print_forecast(forecast):
    for date in forecast:
        print('    ' + date)

# Gets the amount of contracts to buy
def get_amount_to_buy(balance, cost):

    if cost > balance:
        return 0
    if balance < 4000:
        return 1
    else:
        return floor(balance * 0.0005)

# Makes an assumption on the breakeven price
# Breakeven = strike price + option premium
# Since it's not using actual contracts, it will make the strike price the stock price
# Stock price should be in the hundreds or whatever it is - $400
# Also, strike prices on WeBull usually start at the floor and move down, at the next number up
# Contract price should be the full price - $400
def get_breakeven(stock_price, contract_price, trend):
    return floor(stock_price) + ((contract_price/100) * trend)

def get_trend(close, open):
    return copysign(1, close-open)

# You can only lose the amount that you paid for the premium
# If the max loss is less, then you lose that
# If the max loss is higher, then you lose the premium
def get_loss(loss, contract_cost, amount):
    if loss < contract_cost:
        return loss
    else:
        return contract_cost * amount

# Loops through the daily data - DAYS
# Checks if the days after n_days goes in the opposite direction
# If so, count it and add profit
# If not, don't count it and lose money
# Returns a dictionary with the results
def test_ndays_swing(n_days: int, s_balance: float, c_cost: float, delta: float):

    start_day  = None
    last_day   = None
    start      = False
    balance    = s_balance
    count      = 0 # How many times its checked 
    correct    = 0 # How many times its write
    differences = [] # $ value of changes when there is a swing

    for index, day in enumerate(DAYS):
        
        # Don't run if index+1 is out of range
        if index <= len(DAYS)-2:

            # Don't start counting until at least 1 swing has happened
            # Really just checking for a small direction change
            if is_swing(day, DAYS[index+1]):
                start     = True

                if start_day == None:
                    start_day = day

            if index % n_days == 0 and start == True:
                count         = count + 1 # Add count
                current_trend = get_trend(day.close, day.open)
                difference    = DAYS[index+1].close - DAYS[index+1].open
                to_buy        = get_amount_to_buy(balance, c_cost)

                # If the signs are different, then the candles are different
                # Means it swung back the other direction
                if is_swing(day, DAYS[index+1]):
                    correct  = correct + 1
                    last_day = day
                    profit   = (abs(difference) * 100 * delta * to_buy)
                    balance  = balance + profit
                    differences.append(abs(difference))
                else:
                    c_loss  = (abs(difference) * 100 * delta * to_buy) # Calculated loss
                    a_loss  = get_loss(c_loss, c_cost, to_buy) # Actual loss
                    balance = balance - a_loss

    percentage     = round(correct/count*100, 2)
    avg_difference = round(statistics.mean(differences),2)
    forecast       = get_forecast(last_day.date, 10, n_days)

    d = dict()
    d['Start Date']    = start_day.date
    d['Start Balance'] = round(s_balance, 2)
    d['N Days']        = n_days
    d['Count']         = count
    d['Correct']       = correct
    d['Percentage']    = percentage
    d['AVG $ Change']  = avg_difference
    d['Last Date']     = last_day.date
    d['End Balance']   = round(balance, 2)
    d['Forecast']      = forecast

    return d

# Will test the swing tester a certain number of times to determine the best n_days
# This will go based on the highest ending balance - eb
def test_tester_eb(times, s_balance=S_BALANCE_DEFAULT,c_cost=C_COST_DEFAULT,delta=DELTA_DEFAULT):
    best_n    = None
    results   = None
    for n in range(1, times, 1):
        r = test_ndays_swing(n, s_balance, c_cost, delta)

        if best_n == None and results == None:
            best_n  = n
            results = r
        elif r['End Balance'] > results['End Balance']:
            best_n  = n 
            results = r

    d = dict()
    d['Best N']  = best_n
    d['Results'] = results

    return d

# Another tester but looks for the highest chance
def test_tester_hp(times, s_balance=S_BALANCE_DEFAULT,c_cost=C_COST_DEFAULT,delta=DELTA_DEFAULT):
    best_n    = None
    results   = None
    for n in range(1, times, 1):
        r = test_ndays_swing(n, s_balance, c_cost, delta)

        if best_n == None and results == None:
            best_n  = n
            results = r
        elif r['Percentage'] > results['Percentage']:
            best_n  = n 
            results = r

    d = dict()
    d['Best N']  = best_n
    d['Results'] = results

    return d

# Looks for the best delta based on the n value
# Best delta is what returns the highest end balance
def test_tester_delta(n, s_balance=S_BALANCE_DEFAULT,c_cost=C_COST_DEFAULT):
    best_d    = None
    results   = None

    for d in np.arange(0.20, 0.75, .01):
        r = test_ndays_swing(n, s_balance, c_cost, d)

        if best_d == None and results == None:
            best_d  = d
            results = r
        elif r['End Balance'] > results['End Balance']:
            best_d  = d 
            results = r

    d = dict()
    d['Best Delta']  = best_d
    d['Results'] = results

    return d

# --- CODE --- #
print('\n--- It\'s lights out and away we go! ---')

swing_test  = test_ndays_swing(7, 1000, 240, 0.40)
best_n_days = test_tester_eb(30)
print(swing_test)

print('--- It\'s all over! ---\n')