import statistics
from csv_reader import get_days

DAYS = get_days('./data/spy_daily_since_2021.csv')

# Finds the average dollar movement
# Needs daily data, not intraday
def get_avg_range(days):

    changes = []

    for day in days:
        change = abs(day.close - day.open)
        changes.append(change)
    
    return round(statistics.mean(changes),2)

average = get_avg_range(DAYS)
print(average)