import math
from multiprocessing.resource_sharer import stop
from file_reader import get_days
from classes import Result
from json_handler import get_dict
from datetime import datetime
from options_handler import get_options_by_date

# Constants
DAYS    = get_days('./data/historical_data_1m.csv') # Historical data in days
OPTIONS = get_dict('./data/spy_options_data.json')  # Historical options for SPY

first_day = DAYS[0]
formatted_date = datetime.strptime(first_day.date, '%m/%d/%y').strftime('%Y-%m-%d') # To match options date

testing = get_options_by_date(formatted_date, OPTIONS)

print('Finished')
