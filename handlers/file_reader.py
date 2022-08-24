import csv
import sys

sys.path.insert(0, '../classes')

from .classes import Interval, Day, DailyDay

def get_days_daily(path):
    days =[]

    with open(path, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)

        for row in reader:
            days.append(DailyDay(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return days

def get_days(path):

    days = []
    day  = Day('', [])
    addIntervals = False

    # Read CSV File
    with open(path, 'r') as infile:
        reader = csv.reader(infile) # Reads one line at a time
        header = next(reader) # Takes the current row, converts to list, advances to next row
        
        # Loop through entries in CSV File
        for row in reader:

            print(type(row))
            # Get time
            time = row[1]

            # Check if it's the start of the market - 09:30:AM
            if time == '9:28' or time == '9:29' or time == '9:30' or time == '9:31' or time == '9:32':
                addIntervals = True
            elif time == '16:01':
                addIntervals = False

            if addIntervals == True:

                # Check interval date for a new day
                if len(day.intervals) >= 2:
                    lastDate = day.intervals[len(day.intervals)-1].date

                    # Compare current date to the last date saved
                    # If not the same, append the day and reset it
                    if row[0] != lastDate:
                        days.append(day)
                        day = Day('',[])
                    
                # Create interval object
                interval = Interval(row[0], row[1], float(row[2]), float(row[3]), float(row[4]), float(row[5]))
                
                # Add interval to day
                day.add_interval(interval)
                day.set_date(interval.date)

    return days