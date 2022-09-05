from datetime import date
from dateutil.relativedelta import relativedelta
from csv_reader import get_days_from, get_eod_data
from stock_analyzer import print_list, get_avg_range, get_best_nday, map_best_ndays, trend_trade_chance_ndays, best_trend_trade_chance, days_before_opp_dir
from stock_trader import trade_ndays, get_best_trade_results

# Get data 3 years from today
to_date   = date.today().strftime('%Y-%m-%d')
from_date = (date.today() - relativedelta(years=3)).strftime('%Y-%m-%d')
days      = get_eod_data(from_date, to_date, '')