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
                self.sell(tp=0.9*price, sl=1.05*price)
        elif crossover(self.daily_rsi, self.lower_bound):
            if self.position.is_short or not self.position:
                self.position.close()
                self.buy(tp=1.1*price, sl=0.95*price)

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

    fastperiod = 12
    slowperiod = 26
    signalperiod = 9

    def init(self):
        self.macdsignal = self.I(talib.MACD, self.data.Close, self.fastperiod, self.slowperiod, self.signalperiod)

    def next(self):
        price = self.data.Close[-1]
        if crossover(self.macdsignal[1], self.macdsignal[0]):
            self.position.close()
            self.buy()
        elif crossover(self.macdsignal[0], self.macdsignal[1]):
            self.position.close()
            self.sell()


def indicator(data, period=7, multiplier=100):
    return data.Close.s.pct_change(periods=period) * multiplier

class OSMA(Strategy):
    period = 7
    multiplier = 100
    def init(self):
        self.pct_change = self.I(indicator, self.data, period=self.period, multiplier=self.multiplier)
        
        
    def next(self):
        change = self.pct_change[-1]

        if self.position:
            if change < 0:
                self.position.close()

        else:
            if change > 5 and self.pct_change[-2] > 5:
                self.buy()



# def maindicator(data, period=5):
#     # Slice the data to get only the relevant period
#     data_slice = data[:period]
#     # Calculate the total of the sliced data
#     total = sum(data_slice)
#     # Calculate the simple moving average
#     sma = total / period
#     # Return the calculated SMA values as a Series
#     sma_series = pd.Series([sma] * len(data))

#     return sma_series


import numpy as np

def maindicator(data, period=5):
    # Initialize an empty list to store the SMA values
    sma_values = []
    
    # Iterate through the data, starting from the (period-1)-th index
    for i in range(period-1, len(data)):
        # Slice the data to get the relevant period
        data_slice = data[i+1-period:i+1]
        # Calculate the total of the sliced data
        total = sum(data_slice)
        # Calculate the simple moving average for the current day
        sma = total / period
        # Append the calculated SMA value to the list
        sma_values.append(sma)
    
    # Pad the SMA values list with NaN values for the initial (period-1) days
    sma_values = [np.nan]*(period-1) + sma_values
    
    # Return the calculated SMA values as a Series
    sma_series = pd.Series(sma_values)

    return sma_series





class OWNSMA(Strategy):

    fastperiod = 5
    slowperiod = 20

    def init(self):
        self.fastmovingaverage = self.I(maindicator, data=self.data.Close, period=self.fastperiod)
        self.slowmovingaverage = self.I(maindicator, data=self.data.Close, period=self.slowperiod)

    def next(self):
        if self.fastmovingaverage > self.slowmovingaverage:
            self.buy()
        elif self.slowmovingaverage > self.fastmovingaverage:
            self.position.close()

    # def next(self):
    #     if crossover(self.fastmovingaverage, self.slowmovingaverage):
    #         self.buy()
    #     elif crossover(self.slowmovingaverage, self.fastmovingaverage):
    #         self.position.close()




        
#bt = Backtest(GOOG, RsiOscillator, cash = 10_000)
#bt = Backtest(BTC, SMA_MovingAverage, cash = 10_000)
#bt = Backtest(GOOG, ADX, cash = 10_000)
#bt = Backtest(GOOG, STOCH, cash = 10_000)
#bt = Backtest(GOOG, MACD, cash=10_000)
#bt = Backtest(BTC, OSMA, cash=10_000)
bt = Backtest(GOOG, OWNSMA, cash=10_000)

# stats = bt.optimize(
#     fastperiod = range(5,20,5),
#     slowperiod = range(15,30,5),
#     signalperiod = range(3,15,3)
# )

#'''
# stats = bt.optimize(
#     upper_bound = range(55, 85, 5),
#     lower_bound = range(10, 45, 5),
#     rsi_window = range(10,30,5),
#     maximize = optim_func)
    # own custom maximization function
    #maximize = optim_func,
    #constraint = lambda param: param.upper_bound > param.lower_bound,
    # less then optimizers that have to be run so randomizes grid search
    #max_tries = 50)
#print(stats)
#'''

stats = bt.optimize(
    fastperiod = range(2,30),
    slowperiod = range(20,80, 5),
    maximize = optim_func)



#bt.run()
bt.plot(filename='./tests')
print(stats)
print(stats['_strategy'])
