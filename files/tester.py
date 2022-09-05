import os
from dotenv import load_dotenv
from datetime import date
from dateutil.relativedelta import relativedelta
from csv_reader import get_eod_data
from stock_analyzer import get_counter_data_from, get_chance_from
from stock_trader import trade_with_chance

# Get API key
load_dotenv()
API_KEY = os.getenv('API_KEY')

# Get data 3 years from today
to_date      = date.today().strftime('%Y-%m-%d')
from_date    = (date.today() - relativedelta(years=3)).strftime('%Y-%m-%d')
days         = get_eod_data(from_date, to_date, API_KEY)

# Get counter data based on the days provided
counter_data = get_counter_data_from(days)

# Simulate trades to determine probability
trade_with_chance(days, counter_data, get_chance_from)
