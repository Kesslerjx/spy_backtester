from csv_reader import get_days
from stock_analyzer import print_list, get_avg_range, get_opp_dir_chance, get_best_nday, map_best_ndays

ford_days       = get_days('./data/ford_daily_since_2021.csv')
ford_avg_range  = get_avg_range(ford_days)
ford_best_n     = get_best_nday(ford_days)
ford_best_ndays = map_best_ndays(ford_days)

print_list(ford_best_ndays)