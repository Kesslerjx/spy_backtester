from csv_reader import get_days
from stock_analyzer import print_list, get_avg_range, get_best_nday, map_best_ndays, trend_trade_chance_ndays, best_trend_trade_chance, avg_days_before_opp_dir
from stock_trader import trade_ndays, get_best_trade_results

stock_days    = get_days('./data/spy_daily_since_2022.csv')
avg_days = avg_days_before_opp_dir(stock_days)
print(avg_days)