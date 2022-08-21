import math
from multiprocessing.resource_sharer import stop
from file_reader import get_days
from classes import Result
from json_handler import get_dict
from datetime import datetime
from options_handler import get_options_by_date, get_itm_calls, get_near_price_calls, get_options_ndays_out, remove_zero_deltas

# Matches the style of the options JSON data
def date_formatter(date):
    return datetime.strptime(date, '%m/%d/%y').strftime('%Y-%m-%d')

# Constants
DAYS    = get_days('./data/historical_data_1m.csv') # Historical data in days
OPTIONS = get_dict('./data/spy_options_data.json')  # Historical options for SPY

for day in DAYS:
    day_open_price = day.intervals[0].open
    formatted_date = date_formatter(day.date)

    todays_options = get_options_by_date(formatted_date, OPTIONS)
    five_days_out  = get_options_ndays_out(formatted_date, 5, OPTIONS)
    near_price     = get_near_price_calls(todays_options, day_open_price)
    itm_calls      = get_itm_calls(todays_options)
    zero_deltas    = remove_zero_deltas(five_days_out['PUT'])
    