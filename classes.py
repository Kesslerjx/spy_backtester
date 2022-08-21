
class Interval:
    def __init__(self, date, time, open, high, low, close) -> None:
        self.date  = date
        self.time  = time
        self.open  = open
        self.high  = high
        self.low   = low
        self.close = close

class Day:
    def __init__(self, date, intervals) -> None:
        self.date      = date
        self.intervals = intervals

    def add_interval(self, interval):
        self.intervals.append(interval)

    def set_date(self, date):
        self.date = date

    def reset_var(self):
        self.date = ''
        self.intervals = []


class Result:
    def __init__(self, win, change, balance, date, interval, takeProfit, stopLoss) -> None:
        self.win        = win
        self.change     = change
        self.balance    = balance
        self.date       = date
        self.interval   = interval
        self.takeProfit = takeProfit
        self.stopLoss   = stopLoss

    def show_result(self):
        print('')
        print(self.date)
        if self.win: print('Win')
        else: print('Lose')
        print('End Balance: ' + str(self.balance))
        print('Open: ' + str(self.interval.open))
        print('High: ' + str(self.interval.high))
        print('Low: ' + str(self.interval.low))
        print('Take Profit: ' + str(self.takeProfit))
        print('Stop Loss: ' + str(self.stopLoss))
        print('')