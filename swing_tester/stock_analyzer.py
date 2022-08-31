import statistics

# Finds the average dollar movement
# Needs daily data, not intraday
def get_avg_range(days):

    changes = []

    for day in days:
        change = abs(day.close - day.open)
        changes.append(change)
    
    return round(statistics.mean(changes),2)
