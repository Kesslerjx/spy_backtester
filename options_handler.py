from datetime import datetime, timedelta
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
def get_options_by_date(date, options_dict, options=[], count=0):
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
# Stop if options are found or if there is nothing else to check
def get_options_ndays_out(date, days, options_dict, options=[], count=0):
    if len(options) > 0:
        return options[0][OPTIONS_KEY]
    elif count == len(options_dict):
        return options
    else:
        # Get the date the requested number of days away
        requestedDate = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days)).strftime('%Y-%m-%d')

        # Filter by comparing expriation date to next date
        for data in options_dict[DATA_KEY]:
                if data[EXPIRATION_KEY] == requestedDate:
                    options.append(data)
        
        # Increase run count
        count += 1

        # Use recursion to step through days until some options are found
        # If not requested date doesn't have any options, it will step by 1 until some are found
        # If options are found, options length will be greater than 0 and will terminate the recursion
        return get_options_ndays_out(requestedDate, 1, options_dict, options, count)

# Gets call options that are marked as in the money     
def get_itm_calls(options):
    calls = []

    for call in options[CALLS_KEY]:
        if call[ITM_KEY] == 'TRUE':
            calls.append(call)

    return calls  

# Gets calls that are within plus 1 minus 1 of the price passed in
def get_near_price_calls(options, current_price):
    calls = []

    for call in options[CALLS_KEY]:
        if float(call[STRIKE_KEY]) == math.floor(current_price)-1 or float(call[STRIKE_KEY]) == math.floor(current_price)+1 or float(call[STRIKE_KEY]) == math.floor(current_price):
            calls.append(call)
    
    return calls

def remove_zero_deltas(options):
    pruned = []

    # Prune calls
    for option in options:
        print(type(option[DELTA_KEY]))
        if abs(float(option[DELTA_KEY])) > float('0'):
            pruned.append(option)

    return pruned

