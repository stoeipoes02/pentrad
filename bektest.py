from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, barssince
import talib
import numpy as np
import pandas as pd

# importing daily btc candles from investing.com
BTC = pd.read_csv('BTChistorical.csv')
BTC = BTC.drop(columns=['Change %'])

BTCTEST = pd.read_csv('BTCTEST.csv')
BTCTEST['Date'] = pd.to_datetime(BTCTEST['Date'])

BTCTEST.set_index("Date", inplace=True)


print(BTCTEST.head())
#print(BTC.head())
print(GOOG.head())

# Display the dataframe in "CSV" format with column names
#print(GOOG.to_string(header=True, index=True, index_names=True, justify="right"))


def optim_func(series):
    # make things more fun
    if series["# Trades"] < 20:
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
        price = self.data.Close[-1]

        if crossover(self.daily_rsi, self.upper_bound):
            if self.position.is_long or not self.position:
                self.position.close()
                self.sell()
        elif crossover(self.daily_rsi, self.lower_bound):
            if self.position.is_short or not self.position:
                self.position.close()
                self.buy()
''' def next(self):

        if crossover(self.daily_rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.daily_rsi):
            self.buy()
'''

'''
        price = self.data.Close[-1]

        if (self.daily_rsi[-1] > self.upper_bound and barssince(self.daily_rsi < self.upper_bound) == 3):
            self.position.close()

        elif self.lower_bound > self.daily_rsi[-1]:
            self.buy(size=1)


        # elif crossover(self.lower_bound, self.daily_rsi):
        #     #self.buy(tp=1.15*price,sl=0.95*price)
        #     self.buy(size=0.1)
'''

class SMA_MovingAverage(Strategy):

    sma_10window = 10
    sma_50window = 50

    def init(self):
        self.fastmovingaverage = self.I(talib.SMA, self.data.Close, self.sma_10window)
        self.slowmovingaverage = self.I(talib.SMA, self.data.Close, self.sma_50window)
   
    def next(self):

        if self.fastmovingaverage < self.slowmovingaverage:
            self.position.close()
    
        elif self.fastmovingaverage > self.slowmovingaverage:
            self.buy()

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
        
#bt = Backtest(BTCTEST, RsiOscillator, cash = 10_000_000)
#bt = Backtest(GOOG, SMA_MovingAverage, cash = 10_000)
#bt = Backtest(GOOG, ADX, cash = 10_000)
#bt = Backtest(GOOG, STOCH, cash = 10_000)
#bt = Backtest(GOOG, MACD, cash=10_000)


'''
stats = bt.optimize(
    upper_bound = range(55, 85, 5),
    lower_bound = range(10, 45, 5),
    rsi_window = range(10,30,2),
    #maximize = 'Sharpe Ratio',
    # own custom maximization function
    maximize = optim_func,
    constraint = lambda param: param.upper_bound > param.lower_bound,
    # less then optimizers that have to be run so randomizes grid search
    max_tries = 50)
#'''
#print(stats)

# stats = bt.run()
# bt.plot(filename='./tests')
# print(stats)
# print(stats['_strategy'])
