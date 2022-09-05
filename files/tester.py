import os
from dotenv import load_dotenv
from datetime import date
from dateutil.relativedelta import relativedelta
from csv_reader import get_eod_data
from stock_analyzer import days_before_opp_dir

# Get API key
API_KEY = os.getenv('API_KEY')

# Get data 3 years from today
to_date   = date.today().strftime('%Y-%m-%d')
from_date = (date.today() - relativedelta(years=3)).strftime('%Y-%m-%d')
days      = get_eod_data(from_date, to_date, API_KEY)
days_data = days_before_opp_dir(days)

print(days_data)