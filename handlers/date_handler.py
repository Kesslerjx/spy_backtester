from datetime import datetime, timedelta

# Matches the style of the options JSON data
def date_formatter(date):
    return string_to_date(date).strftime('%Y-%m-%d')

def days_between(from_date, to_date):
    return (string_to_date(to_date) - string_to_date(from_date)).days

def string_to_date(date):
    return datetime.strptime(date, '%m/%d/%y')

def add_days_to_date(date, days):
    date_as_date = datetime.strptime(date, '%Y-%m-%d')
    days_delta   = timedelta(days)
    new_date     = date_as_date + days_delta
    date_string  = new_date.strftime('%Y-%m-%d')
    return date_string