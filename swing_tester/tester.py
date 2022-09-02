from csv_reader import get_days
from stock_analyzer import print_list, get_avg_range, get_best_nday, map_best_ndays
from stock_trader import trade_ndays, get_best_trade_results

stock_days    = get_days('./data/spy_daily_since_2018.csv')
best_nday     = get_best_nday(stock_days)
trade_results = trade_ndays(stock_days, 5000, 2)

best_trade_results = get_best_trade_results(stock_days, 5000)

print(best_nday)
print(best_trade_results)