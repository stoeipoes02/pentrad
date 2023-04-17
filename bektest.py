from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, barssince
from datetime import datetime
import talib
import numpy as np
import pandas as pd

'''
Issues:
1. optimizing doesnt work properly on sma
'''


# importing daily btc candles from investing.com
BTC = pd.read_csv('BTChistorical.csv')


# converts the string from "Apr 07, 2023" to 2023-04-07
def convert_date(date_string):
    date_object = datetime.strptime(date_string, "%b %d, %Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date
# applies the above function to the dataframe
BTC["Date"] = BTC["Date"].apply(convert_date)


# changes the date from a string to datetime and sets this datetime as index for the dataframe
BTC['Date'] = pd.to_datetime(BTC['Date'])
BTC.set_index("Date", inplace=True)


# List of columns to update
columns_to_update = ["Open", "High", "Low","Close"]
# Loop through the columns and remove double quotes and commas, and convert to float
for col in columns_to_update:
    BTC[col] = BTC[col].str.replace('"', '').str.replace(',', '').astype(float)


# replaces the values in volume to their appropriate decimal count
suffixes = {"K": 3, "M": 6, "B": 9, "T": 12}
def replace_suffix_with_multiplier(value):
    for suffix, multiplier in suffixes.items():
        if value.endswith(suffix):
            return int(float(value[:-1]) * 10 ** multiplier)
    return int(value)
BTC["Volume"] = BTC["Volume"].map(replace_suffix_with_multiplier)


# reverses the entire dataframe because backtesting.py works with oldest date at the top
BTC = BTC.iloc[::-1]





def optim_func(series):
    # make things more fun
    if series["# Trades"] < 30:
        # puts value low so will try to optimize more
        return -1

    # how to make most money while being in the market for least amount of time
    #return series['Equity Final [$]'] / series["Exposure Time [%]"]

    return series['Sharpe Ratio']


class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.daily_rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)


    def next(self):
        if crossover(self.daily_rsi, self.upper_bound):
            if self.position.is_long or not self.position:
                self.position.close()
                self.sell()
        elif crossover(self.daily_rsi, self.lower_bound):
            if self.position.is_short or not self.position:
                self.position.close()
                self.buy()

        # price = self.data.Close[-1]

        # if (self.daily_rsi[-1] > self.upper_bound and barssince(self.daily_rsi < self.upper_bound) == 3):
        #     self.position.close()

        # elif self.lower_bound > self.daily_rsi[-1]:
        #     self.buy(size=1)


        # # elif crossover(self.lower_bound, self.daily_rsi):
        # #     #self.buy(tp=1.15*price,sl=0.95*price)
        # #     self.buy(size=0.1)

class SMA_MovingAverage(Strategy):
    fastmovingaverage = 10
    slowmovingaverage = 50

    def init(self):
        self.fastmovingaverage = self.I(talib.SMA, self.data.Close, self.fastmovingaverage)
        self.slowmovingaverage = self.I(talib.SMA, self.data.Close, self.slowmovingaverage)


    def next(self):
        if crossover(self.fastmovingaverage,self.slowmovingaverage):
            self.buy()
        elif crossover(self.slowmovingaverage,self.fastmovingaverage):
            self.position.close()

        # elif crossover(self.lower_bound, self.daily_rsi):
        #     #self.buy(tp=1.15*price,sl=0.95*price) 
        #     self.buy(size=0.1)

class ADX(Strategy):

    def init(self):
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, 14)
    
    def next(self):
        if self.adx > 25:
            self.buy()
        else:
            self.position.close()

class STOCH(Strategy):

    def init(self):
        self.stoch = self.I(talib.STOCH,self.data.High, self.data.Low, self.data.Close, 5, 3, 0, 3, 0)

    def next(self):
        if self.data.index[-1].year == 2008:
            self.position.close()
            return

        if self.stoch[0] > self.stoch[1]:
            self.buy()
        else:
            self.position.close()

class MACD(Strategy):

    def __init__(self, fastperiod, slowperiod, signalperiod):
        self.fastperiod = fastperiod
        self.slowperiod = slowperiod
        self.signalperiod = signalperiod

    def init(self):
        self.macdsignal = self.I(talib.MACD, self.data.Close, self.fastperiod, self.slowperiod, self.signalperiod)

    def next(self):
        if self.macdsignal[1] > self.macdsignal[0] and not self.position:
            self.buy()
        elif self.macdsignal[0] > self.macdsignal[1]:
            self.position.close()


BTC['Signal'] = np.random.randint(-1,2, len(BTC))

import pandas_ta as ta


# upperband, middleband, lowerband = BBANDS(close, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)

def indicator(data):
    return data.Close.s.pct_change(periods=7) * 100

class OSMA(Strategy):
    def init(self):
        self.pct_change = self.I(indicator, self.data)
        
        
    def next(self):
        change = self.pct_change[-1]

        if self.position:
            if change < 0:
                self.position.close()

        else:
            if change > 5 and self.pct_change[-2] > 5:
                self.buy()


        
#bt = Backtest(GOOG, RsiOscillator, cash = 10_000)
#bt = Backtest(BTC, SMA_MovingAverage, cash = 10_000)
#bt = Backtest(GOOG, ADX, cash = 10_000)
#bt = Backtest(GOOG, STOCH, cash = 10_000)
#bt = Backtest(GOOG, MACD, cash=10_000)
#bt = Backtest(BTC, backtoback, cash=10_000)
bt = Backtest(BTC, OSMA, cash=10_000)



'''
stats = bt.optimize(
    upper_bound = range(55, 85, 5),
    lower_bound = range(10, 45, 5),
    rsi_window = range(10,30,2),
    maximize = 'Sharpe Ratio',
    # own custom maximization function
    #maximize = optim_func,
    #constraint = lambda param: param.upper_bound > param.lower_bound,
    # less then optimizers that have to be run so randomizes grid search
    max_tries = 50)
#print(stats)
'''

# stats = bt.optimize(
#     fastmovingaverage = range(8,12),
#     slowmovingaverage = range(46,54),
#     maximize = 'Sharpe Ratio',#optim_func,
#     max_tries = 50
# )

stats = bt.run()
bt.plot(filename='./tests')
print(stats)
print(stats['_strategy'])

    
    

