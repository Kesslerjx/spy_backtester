import statistics
import holidays
from math import copysign
from csv_reader import get_days
from datetime import datetime, timedelta

# Returns true if a swing
# Returns false if not
def is_swing(current_candle, next_candle):
    return copysign(1, current_candle) != copysign(1, next_candle)

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
    return not(is_holiday(date)) or not(is_weekend(date))

def get_forecast(start_date, amount, days):
    forecast = []
    f_count = 1
    d_count = 1

    while f_count <= amount:

        while d_count <= days:
            # Add a day
            start_date = add_day(start_date)
            # Only count the day if it's a business day
            if is_business_day(add_day(start_date)):
                d_count = d_count + 1

        forecast.append(start_date)
        d_count = 1
        f_count = f_count + 1 

    return forecast

def print_forecast(forecast):
    for date in forecast:
        print('    ' + date)

# Get the days from the CSV file
# Get holidays for forecasting purposes
DAYS     = get_days('./data/spy_daily_since_2021.csv')
HOLIDAYS = holidays.US()

start_day  = None
last_day   = None
start      = False
n_days     = 7 # Number of days to test for a swing
count      = 0 # How many times its checked 
correct    = 0 # How many times its write
differences = [] # $ value of changes when there is a swing

print('\n--- It\'s lights out and away we go! ---')

for index, day in enumerate(DAYS):
    
    # Don't run if index+1 is out of range
    if index <= len(DAYS)-2:

        # Don't start counting until at least 1 swing has happened
        # Really just checking for a small direction change
        if is_swing(day.close - day.open, DAYS[index+1].close - DAYS[index+1].open):
            start     = True

            if start_day == None:
                start_day = day

        if index % n_days == 0 and start == True:
            count = count + 1 # Add count

            # If the signs are different, then the candles are different
            # Means it swung back the other direction
            if is_swing(day.close - day.open, DAYS[index+1].close - DAYS[index+1].open):
                correct    = correct + 1
                last_day   = day
                difference = DAYS[index+1].close - day.close
                differences.append(abs(difference))

percentage     = round(correct/count*100, 2)
avg_difference = round(statistics.mean(differences),2)
forecast       = get_forecast(last_day.date, 10, n_days)

print('Start Date:       ' + start_day.date)
print('Number of Days:   ' + str(n_days))
print('Count:            ' + str(count))
print('Correct:          ' + str(correct))
print('Percentage:       ' + str(percentage) + '%')
print('Average $ Change: ' + str(avg_difference))
print('Last Date:        ' + last_day.date)
print('Next 10 Dates:')
print_forecast(forecast)   
print('--- It\'s all over! ---\n')