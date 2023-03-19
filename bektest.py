from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, barssince
import talib
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from matplotlib import pyplot



class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.daily_rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    def next(self):

        price = self.data.Close[-1]

        if (self.daily_rsi[-1] > self.upper_bound and barssince(self.daily_rsi < self.upper_bound) == 3):
            self.position.close()

        elif self.lower_bound > self.daily_rsi[-1]:
            self.buy(size=1)


        # elif crossover(self.lower_bound, self.daily_rsi):
        #     #self.buy(tp=1.15*price,sl=0.95*price)
        #     self.buy(size=0.1)

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

    fastperiod = 12
    slowperiod = 26
    signalperiod = 9

    def init(self):
        self.macdsignal = self.I(talib.MACD, self.data.Close, self.fastperiod, self.slowperiod, self.signalperiod)

    def next(self):
        if self.macdsignal[1] > self.macdsignal[0] and not self.position:
            self.buy()
        elif self.macdsignal[0] > self.macdsignal[1]:
            self.position.close()
        
class PATTERN(Strategy):
    def init(self):
        pass

    def next(self):
        pass
#bt = Backtest(GOOG, RsiOscillator, cash = 10_000)
#bt = Backtest(GOOG, SMA_MovingAverage, cash = 10_000)
#bt = Backtest(GOOG, ADX, cash = 10_000)
#bt = Backtest(GOOG, STOCH, cash = 10_000)
bt = Backtest(GOOG, MACD, cash=10_000)


# stats = bt.run()
# bt.plot()
# print(stats)


# reading in the data
df = pd.read_csv("EURUSD_Candlestick_4_Hour_ASK_05.05.2003-16.10.2021.csv")
df.columns=['time', 'open', 'high', 'low', 'close', 'volume']
#Check if NA values are in data
df=df[df['volume']!=0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()




backcandles= 100
brange = 50 #should be less than backcandles
wind = 5

candleid = 10100

optbackcandles = backcandles
sldiff = 100
sldist = 10000
for r1 in range(backcandles-brange, backcandles+brange):
    maxim = np.array([])
    minim = np.array([])
    xxmin = np.array([])
    xxmax = np.array([])
    
    for i in range(candleid-r1, candleid+1, wind):
        minim = np.append(minim, df.low.iloc[i:i+wind].min())
        xxmin = np.append(xxmin, df.low.iloc[i:i+wind].idxmin())
    for i in range(candleid-r1, candleid+1, wind):
        maxim = np.append(maxim, df.high.loc[i:i+wind].max())
        xxmax = np.append(xxmax, df.high.iloc[i:i+wind].idxmax())
    slmin, intercmin = np.polyfit(xxmin, minim,1)
    slmax, intercmax = np.polyfit(xxmax, maxim,1)
    
    dist = (slmax*candleid + intercmax)-(slmin*candleid + intercmin)
    if(dist<sldist): #abs(slmin-slmax)<sldiff and
        #sldiff = abs(slmin-slmax)
        sldist = dist
        optbackcandles=r1
        slminopt = slmin
        slmaxopt = slmax
        intercminopt = intercmin
        intercmaxopt = intercmax
        maximopt = maxim.copy()
        minimopt = minim.copy()
        xxminopt = xxmin.copy()
        xxmaxopt = xxmax.copy()

        
print(optbackcandles)
dfpl = df[candleid-wind-optbackcandles-backcandles:candleid+optbackcandles]  
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])

adjintercmax = (df.high.iloc[xxmaxopt] - slmaxopt*xxmaxopt).max()
adjintercmin = (df.low.iloc[xxminopt] - slminopt*xxminopt).min()
fig.add_trace(go.Scatter(x=xxminopt, y=slminopt*xxminopt + adjintercmin, mode='lines', name='min slope'))
fig.add_trace(go.Scatter(x=xxmaxopt, y=slmaxopt*xxmaxopt + adjintercmax, mode='lines', name='max slope'))
fig.show()