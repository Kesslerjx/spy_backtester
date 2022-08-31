from math import copysign
import statistics

# Finds the average dollar movement
# Needs daily data, not intraday
def get_avg_range(days):

    changes = []

    for day in days:
        change = abs(day.close - day.open)
        changes.append(change)
    
    return round(statistics.mean(changes),2)

# Finds the chance of the stock price going the opposite direction every n_days
def get_opp_dir_chance(days, n_day):
    count   = 0
    correct = 0

    # Check if it's the right day to check
    # Get the current day different to find if green or red
    # Same thing for next day
    # If signs are different, then it went the opposite direction
    for index, day in enumerate(days):
        if index % n_day == 0:
            count = count + 1
            # Avoid out of range error
            if index <= len(days)-2:
                current_day = day.close - day.open
                next_day    = days[index+1].close - days[index+1].open
                different   = copysign(1, current_day) == copysign(1, next_day)

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
