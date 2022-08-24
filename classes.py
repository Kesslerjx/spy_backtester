import math

class Interval:
    def __init__(self, date, time, open, high, low, close) -> None:
        self.date  = date
        self.time  = time
        self.open  = open
        self.high  = high
        self.low   = low
        self.close = close

class DailyDay:
    def __init__(self, date, open, high, low, close, adjusted, volume) -> None:
        self.date     = date
        self.open     = float(open)
        self.high     = float(high)
        self.low      = float(low)
        self.close    = float(close)
        self.adjusted = float(adjusted)
        self.volume   = float(volume)

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

class Contract:
    def __init__(self, date, spot, option, trend, amount, risk, reward) -> None:
        self.date   = date
        self.spot   = spot
        self.option = option
        self.trend  = trend
        self.amount = amount
        self.risk   = risk
        self.reward = reward
        self.ask    = option['ask']
        self.bid    = option['bid']
        self.delta  = option['delta']
        self.theta  = option['theta']
        self.price  = float(self.ask) * float(100) * float(amount)
        self.value  = self.bid * 100

        self.take_profit = self.ask + (reward/100)
        self.stop_loss   = self.ask - (risk/100)

        self.set_tp_sl_amounts()

    def theta_decay(self):
        self.ask = self.ask + self.theta
        self.bid = self.bid + self.theta

    def delta_change(self, stock_price):
        price_change  = stock_price - self.spot
        change_amount = price_change * abs(self.delta)

        self.ask   = self.ask + (change_amount * self.trend)
        self.bid   = self.bid + (change_amount * self.trend)
        self.value = self.bid * 100
    
    def set_tp_sl_amounts(self):
        bid_change_tp = self.take_profit - self.bid
        bid_change_sl = self.bid - self.stop_loss
        tp_dollar_change = bid_change_tp / self.delta
        sl_dollar_change = bid_change_sl / self.delta 

        if self.trend > 0:
            self.take_profit_amount = self.spot + abs(tp_dollar_change)
            self.stop_loss_amount   = self.spot - abs(sl_dollar_change)
        else:
            self.take_profit_amount = self.spot - abs(tp_dollar_change)
            self.stop_loss_amount   = self.spot + abs(sl_dollar_change)
        

    def get_contract_value_tp(self):
        return (self.take_profit - self.ask) * 100

class Result:
    def __init__(self, balance, contract, trend) -> None:
        self.balance  = balance
        self.contract = contract
        self.trend    = trend