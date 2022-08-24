from handlers.file_reader import get_days_daily
from handlers.json_handler import get_dict
from handlers.options_handler import deltas_with_minimum, get_contracts_by_trend, get_data, get_daily_trend, get_options_at_expiration, remove_contracts_no_interest, remove_contracts_unaffordable
from handlers.date_handler import add_days_to_date

# Get the days from the CSV file
# Get the options from the JSON file
# Get the data values from the OPTIONS dict
DAYS    = get_days_daily('./data/spy_daily_2022.csv')
OPTIONS = get_dict('./data/spy_options_2022.json')
OPTIONS = get_data(OPTIONS)

# 1  - Loop through each day
# 2  - Set a start date and get the close price
# 3  - Go for N number of days or X amount of dollars of change
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

print('\n--- SCENE ---')

start_day   = None
end_day     = None
trend       = None
contract    = None
balance     = 1000
p_contracts = [] # Contracts previously purchased
n_days      = 5 # Days to look for a contract
c_days      = 5 # Days until a contract expires
d_minimum   = 0.30 # Delta minimum

for index, day in enumerate(DAYS):

    # First set the start date
    # Then set the end date
    # Then start the contract process
    if start_day == None:
        start_day = day
    elif end_day == None:
        if index % n_days == 0:
            end_day = day
    else:
        trend     = get_daily_trend(start_day, end_day)
        exp_date  = add_days_to_date(end_day.date, c_days)
        contracts = get_options_at_expiration(exp_date, OPTIONS)

        # No contracts were found within 10 days
        # End the loop here if no contracts were found
        if contracts == None:
            print('No contracts were found within 10 days')
            break
        else:
            # Filter contracts by trend
            # Reverse the trend for swing trading
            contracts = get_contracts_by_trend(trend*-1, contracts)
            contracts = deltas_with_minimum(d_minimum, contracts) # Remove contracts that don't meet the delta minimum
            contracts = remove_contracts_no_interest(contracts) # Remove contracts that don't have any open interest
            contracts = remove_contracts_unaffordable(balance, contracts) # Remove contracts that aren't affordable
            print('test')

print('--- FIN ---\n')