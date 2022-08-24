from multiprocessing.resource_sharer import stop
from handlers.file_reader import get_days
from classes import Result, Contract
from handlers.json_handler import get_dict
from handlers.options_handler import get_contract_at_strike, deltas_with_minimum, get_options_by_date, get_itm_calls, get_near_price_calls, get_options_ndays_out, remove_zero_deltas, find_trend, get_contracts_by_trend
from handlers.date_handler import date_formatter, days_between


# Constants
DAYS       = get_days('./data/historical_data_1m.csv') # Historical data in days
OPTIONS    = get_dict('./data/spy_options_data.json')  # Historical options for SPY

# Strategy Variables
TREND_DAYS      = 4 # Minimum amount of days to look back for a trend
DELTA_MINIMUM   = 0.55 # Get contracts with this minimum delta
OPTION_EXP_DAYS = 4 # Minimum num of days the option expires
STRIKE_DIFF     = 1 # Get contract with this much away from current price ITM
NUM_CONTRACTS   = 1 # Number of contracts to buy at a time
RISK_AMOUNT     = 41.0 # Dollar amount to risk
REWARD_AMOUT    = 77.0 # Dollar amount to win

balances = []

def get_day(date, days):
    for day in days:
        if day.date == date:
            return day
    
    return None

def get_contract(date, trend, price, exp_days, delta_min, options):
    filtered = get_options_ndays_out(date_formatter(date), exp_days, options) # Get all options

    if len(filtered) == 0:
        return None
    else:
        filtered = get_contracts_by_trend(trend, filtered[0]) # Filter options by trend
        filtered = deltas_with_minimum(delta_min, filtered) # Filter options by delta
        contract = get_contract_at_strike(price, STRIKE_DIFF, trend, filtered) # Get the contract to buy

        # Sometimes a contract isn't found at the strike price
        # Return none to skip to the next day if so
        # Probably should fix this later
        if contract == None:
            return contract
        else:
            return Contract(date, price, contract, trend, NUM_CONTRACTS, RISK_AMOUNT, REWARD_AMOUT)

def interval_stepper(intervals, balance, contract, trend):
    print('Stepping through intervals')
    for interval in intervals:
        # Take profit
        # Use trend to determine when it should be taken
        if trend > 0 and interval.close >= contract.take_profit_amount or trend < 0 and interval.close <= contract.take_profit_amount:
            print('Selling contract for a profit')
            contract.delta_change(contract.take_profit_amount)
            balance  = balance + contract.value
            print('New balance: ' + str(balance))
            contract = None # Reset value
            trend    = None # Reset value
            return Result(balance, contract, trend)
        elif trend > 0 and interval.close <= contract.stop_loss_amount or trend < 0 and interval.close >= contract.take_profit_amount:
            # Lose some money
            print('Selling contract for a loss')
            contract.delta_change(contract.stop_loss_amount)
            balance  = balance + contract.value
            print('New balance: ' + str(balance))
            contract = None # Reset value
            trend    = None # Reset value
            return Result(balance, contract, trend)

    # If here, TP or SL wasn't hit at all
    # Update contract values and return the result
    print('TP or SL wasn\'t hit')
    contract.delta_change(intervals[len(intervals)-1].close)
    contract.theta_decay()
    return Result(balance, contract, trend)
            

def start(balance, index, trend=None, contract=None):
    
    # If index == length of days, stop recursion
    # Get the trend
    # Then get the contract
    # Then start going through intervals
    if index == len(DAYS):
        print('Ending Balance: ' + str(balance))
        print('---Finished---\n')
    elif trend == None:
        return start(balance, index, find_trend(DAYS[index-TREND_DAYS].date, DAYS[index].date, DAYS))
    elif contract == None:
        contract = get_contract(DAYS[index].date, trend, DAYS[index].intervals[0].open, OPTION_EXP_DAYS, DELTA_MINIMUM, OPTIONS)
        
        # If no contracts were found, go to the next day
        # Discard contract if it's not affordable
        if contract == None or contract.price > balance:
            return start(balance, index+1, trend=None, contract=None)
        else:
            return start(balance, index, trend, contract)
    else:
        print('\nContract found')
        print('Date: ' + DAYS[index].date)
        balance = balance - contract.price
        print('New balance: ' + str(balance))
        result = interval_stepper(DAYS[index].intervals, balance, contract, trend)
        index  = index + 1
        return start(result.balance, index, result.trend, result.contract)
        

# Start the tester
# Beginning balance of 1000
# Start at the index of TREND_DAYS
print('\n---Started---')
start(1000, TREND_DAYS)