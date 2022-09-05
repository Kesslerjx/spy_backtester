import csv
import requests

class Day:
    def __init__(self, date, open, high, low, close, adjusted, volume) -> None:
        self.date     = date
        self.open     = float(open)
        self.high     = float(high)
        self.low      = float(low)
        self.close    = float(close)
        self.adjusted = float(adjusted)
        self.volume   = float(volume)

def get_days_from(path):

    with open(path, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        days   = create_days(reader)

    return days

def get_eod_data(from_date: str, to_date: str, api_key: str, stock: str='SPY'):
    API_CALL = 'https://eodhistoricaldata.com/api/eod/' + stock + '.US?api_token=' + api_key + '&from=' + from_date + '&to=' + to_date
    response = requests.get(API_CALL)
    lines    = response.text.splitlines()
    reader   = csv.reader(lines)
    header   = next(reader)
    days     = create_days(reader)

    return days

def create_days(reader):
    days = []

    for row in reader:
            days.append(Day(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    
    return days
