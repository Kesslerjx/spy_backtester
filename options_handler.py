from datetime import datetime, timedelta

# KEYS
DATA_KEY       = 'data'
EXPIRATION_KEY = 'expirationDate'
OPTIONS_KEY    = 'options'

def get_options_by_date(date, options_dict, options=[]):
    if(len(options) > 0):
        return options[0][OPTIONS_KEY]
    else:
        # Filter by comparing expriation date to parameter date
        for data in options_dict[DATA_KEY]:
                if(data[EXPIRATION_KEY] == date):
                    options.append(data)
        
        # Get next day
        nextDay = (datetime.strptime(date, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Use recursion to step through days until some options are found
        # If options are found, options length will be greater than 0 and will terminate the recursion
        return get_options_by_date(nextDay, options_dict, options)
            
        
