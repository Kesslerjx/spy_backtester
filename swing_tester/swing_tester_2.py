from math import copysign
from csv_reader import get_days

# Get the days from the CSV file
DAYS    = get_days('./data/spy_daily_2022.csv')

start_day = None
end_day   = None
n_days    = 5 # Number of days to test for a swing
count     = 0 # How many times its checked
correct   = 0 # How many times its write

print('\n--- It\'s lights out and away we go! ---')

for index, day in enumerate(DAYS):
    
    # Don't run if index+1 is out of range
    if index <= len(DAYS)-2:
        if index % n_days == 0:
            count = count + 1 # Add count

            # Find the candle types
            # Positive if green, negative if red
            current_candle = day.close - day.open
            next_candle    = DAYS[index+1].close - DAYS[index+1].open
            current_sign   = copysign(1, current_candle)
            next_sign      = copysign(1, next_candle)

            # If the signs are different, then the candles are different
            # Means it swung back the other direction
            if current_sign != next_sign:
                correct = correct + 1

percentage = round(correct/count*100, 2)
print('Count:      ' + str(count))
print('Correct:    ' + str(correct))
print('Percentage: ' + str(percentage) + '%')
print('--- It\'s all over! ---\n')