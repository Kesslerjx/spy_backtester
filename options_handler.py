from datetime import date, datetime, timedelta
import math

# KEYS
DATA_KEY       = 'data'
EXPIRATION_KEY = 'expirationDate'
OPTIONS_KEY    = 'options'
CALLS_KEY      = 'CALL'
PUTS_KEY       = 'PUT'
ITM_KEY        = 'inTheMoney'
STRIKE_KEY     = 'strike'
DELTA_KEY      = 'delta'

# Gets options that have an expiration of the requested date
# Stop if options are found or if there is nothing else to check
def get_options_by_date(date: str, options_dict, options=[], count=0):
    if(len(options) > 0):
        return options[0][OPTIONS_KEY]
    elif count == len(options_dict):
        return options
    else:
        # Filter by comparing expriation date to parameter date
        for data in options_dict[DATA_KEY]:
                if(data[EXPIRATION_KEY] == date):
                    options.append(data)

        # Increase run count
        count += 1
        
        # Get next day
        nextDay = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Use recursion to step through days until some options are found
        # It will get the next best date if some aren't available on the requested date
        # If options are found, options length will be greater than 0 and will terminate the recursion
        return get_options_by_date(nextDay, options_dict, options, count)

# Get contracts N days away from the date
# If no contracts are found, return none
def get_options_ndays_out(date: str, days: int, options_dict):

    options = []

    # Get the date the requested number of days away
    requestedDate = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days)).strftime('%Y-%m-%d')

    # Filter by comparing expriation date to next date
    for data in options_dict[DATA_KEY]:
        if data[EXPIRATION_KEY] == requestedDate:
             options.append(data)

    return options

# Gets call options that are marked as in the money     
def get_itm_calls(options):
    calls = []

    for call in options[CALLS_KEY]:
        if call[ITM_KEY] == 'TRUE':
            calls.append(call)

    return calls  

# Gets calls that are within plus 1 minus 1 of the price passed in
def get_near_price_calls(options, current_price: float):
    calls = []

    for call in options[CALLS_KEY]:
        if float(call[STRIKE_KEY]) == math.floor(current_price)-1 or float(call[STRIKE_KEY]) == math.floor(current_price)+1 or float(call[STRIKE_KEY]) == math.floor(current_price):
            calls.append(call)
    
    return calls

def get_contracts_by_trend(trend, options):
    if trend > 0:
        return options[OPTIONS_KEY][CALLS_KEY]
    elif trend < 0:
        return options[OPTIONS_KEY][PUTS_KEY]
    else:
        return []


def get_calls(options):
    return options[CALLS_KEY]

def get_puts(options):
    return options[PUTS_KEY]

# Removes any contracts that have a 0 delta
def remove_zero_deltas(options):
    pruned = []

    # Prune calls
    for option in options:
        if abs(float(option[DELTA_KEY])) > float(0):
            pruned.append(option)

    return pruned

# Gets contracts from the option list with at least a certain number
def deltas_with_minimum(decimal: float, options):
    pruned = []

    for option in options:
        if abs(float(option[DELTA_KEY])) >= float(decimal):
            pruned.append(option)

    return pruned

# Gets a contract at strike price from the list of options
def get_contract_at_strike(price, diff, trend, options):

    strike = math.floor(price)+(diff*trend*-1)

    for option in options:
        if float(option[STRIKE_KEY]) == strike:
            return option

    return None

# Find the overall trend using the close amount on each date
# 1  = Up trend
# 0  = No trend, or values weren't found
# -1 = Down trend
def find_trend(from_date: date, to_date: date, days):
    
    from_close = float(0)
    to_close   = float(0)

    # Look for the from date and to date close value
    for day in days:
        if day.date == from_date:
            from_close = day.intervals[len(day.intervals)-1].close
        elif day.date == to_date:
            to_close   = day.intervals[len(day.intervals)-1].close
    
    # If either value is 0, or they are equal to each other, return 0
    # Stock price isn't going to be 0 (it shouldn't be anyways)
    # copysign returns 1 for the value 0
    if from_close == 0 or to_close == 0 or from_close == to_close:
        return 0
    else:
        return math.copysign(1, to_close - from_close)
    
