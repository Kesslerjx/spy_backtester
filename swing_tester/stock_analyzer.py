from math import copysign
import statistics

def print_list(list):
    for l in list:
        print(l)

# Finds the average dollar movement
# Needs daily data, not intraday
def get_avg_range(days):

    changes = []

    for day in days:
        change = abs(day.close - day.open)
        changes.append(change)
    
    return round(statistics.mean(changes),2)

# Finds the chance of the stock price going the opposite direction every n_days
# Goes based off the previous day
def get_opp_dir_chance(days, n_day):
    count   = 0
    correct = 0

    # Check if it's the right day to check
    # Get the current day different to find if green or red
    # Same thing for next day
    # If signs are different, then it went the opposite direction
    for index, day in enumerate(days):
        if index % n_day == 0:
            count        = count + 1
            current_day  = day.close - day.open
            previous_day = days[index-1].close - days[index-1].open
            different    = not(copysign(1, current_day) == copysign(1, previous_day))

            if different:
                    correct = correct + 1
    
    return round(correct/count*100, 2)

# Finds the best nday to use for the stock thats passed to it
# Returns a dict containing the n value and its chance
def get_best_nday(days, times=30):

    best_chance = None
    best_n      = None

    for n in range(1, times, 1):
        chance = get_opp_dir_chance(days, n)
        if best_n == None:
            best_n      = n
            best_chance = chance
        elif chance > best_chance:
            best_n      = n
            best_chance = chance

    d = dict()
    d['n']      = best_n
    d['chance'] = best_chance

    return d

# Returns a list of dictionaries that consist of the n_day value and it's chance
def map_best_ndays(days, times=30):
    n_chances = []
    for n in range(1, times+1, 1):
        d = dict()

        d['n']      = n
        d['chance'] = get_opp_dir_chance(days, n)

        n_chances.append(d)

    return n_chances

# Looks back n_days to determine a trend
# It will then trade based on that trend
# Counts all correct trades to determine chance
def trend_trade_chance_ndays(days: list, n_days: int):
    
    count   = 0
    correct = 0

    for index, day in enumerate(days):
        if index - n_days >= 0 and index < len(days)-1:
            count += 1
            trend = copysign(1, day.close - days[index-n_days].close)
            guess = copysign(1, days[index+1].close - days[index+1].open) # Next days candle
            if guess == trend:
                correct += 1
    
    chance      = round(correct/count*100, 2)
    result      = dict()
    result['n'] = n_days
    result['c'] = chance

    return result

# Will try times number of days to find the one with the best chance
# Returns a dict with the best result, and the result of every day
def best_trend_trade_chance(days: list, times: int=30):
    best_result = None
    results = []

    for n in range(1, times, 1):
        result = trend_trade_chance_ndays(days, n)
        results.append(result)
        if best_result == None or result['c'] > best_result['c']:
            best_result = result
    
    r = dict()
    r['best']    = best_result
    r['results'] = results

    return r