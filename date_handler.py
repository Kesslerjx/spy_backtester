from datetime import datetime

# Matches the style of the options JSON data
def date_formatter(date):
    return string_to_date(date).strftime('%Y-%m-%d')

def days_between(from_date, to_date):
    return (string_to_date(to_date) - string_to_date(from_date)).days

def string_to_date(date):
    return datetime.strptime(date, '%m/%d/%y')