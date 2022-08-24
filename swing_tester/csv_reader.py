import csv

class Day:
    def __init__(self, date, open, high, low, close, adjusted, volume) -> None:
        self.date     = date
        self.open     = float(open)
        self.high     = float(high)
        self.low      = float(low)
        self.close    = float(close)
        self.adjusted = float(adjusted)
        self.volume   = float(volume)

def get_days(path):
    days =[]

    with open(path, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)

        for row in reader:
            days.append(Day(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return days