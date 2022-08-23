from file_reader import get_days_daily
from json_handler import get_dict
from options_handler import get_data

# Get the days from the CSV file
# Get the options from the JSON file
# Get the data values from the OPTIONS dict
DAYS    = get_days_daily('./data/spy_daily_since_2021.csv')
OPTIONS = get_dict('./data/spy_options_since_2021.json')
OPTIONS = get_data(OPTIONS)

# 1  - Loop through each day
# 2  - Set a start date and get the close price
# 3  - Go for N number of days
# 4  - Set the end date and get the close price
# 5  - Find the trend between the two dates
# 6  - Find a contract that is X number of days out in the opposite direction
# 7  - Determine the required contract value for the T_P and S_L
# 8  - Go to next day
# 9  - Apply theta decay to the ask and bid
# 10 - Apply gamma change to the delta
# 11 - Check if the contract should be closed
# 12 - Take profits or loss
# 13 - Start back at number 2

print('--- FIN ---')