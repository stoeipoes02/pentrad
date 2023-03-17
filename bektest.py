from backtesting import Backtest, Strategy
from backtesting.test import GOOG
from backtesting.lib import crossover, plot_heatmaps, resample_apply, barssince
import talib
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

print(GOOG)

def optim_func(series):

    if series['# Trades'] >10:
        return -1

    return series['Equity Final [$]'] / series['Exposure Time [%]']

class RsiOscillator(Strategy):

    upper_bound = 70
    lower_bound = 30
    rsi_window = 14


    def init(self):
        self.daily_rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

        #self.weekly_rsi = resample_apply(
        #    "W-FRI", talib.RSI, self.data.Close, self.rsi_window)

    
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


class Combination(Strategy):

    fastsma = 10
    slowsma = 50

    upper_bound = 70
    lower_bound = 40
    rsi_window = 14

    def init(self):
        self.daily_rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)
        self.fastmovingaverage = self.I(talib.SMA, self.data.Close, self.fastsma)
        self.slowmovingaverage = self.I(talib.SMA, self.data.Close, self.slowsma)

    def next(self):

        if self.fastmovingaverage < self.slowmovingaverage and self.daily_rsi > self.upper_bound:
            self.position.close()
        

        elif self.fastmovingaverage > self.slowmovingaverage:
            self.buy()




#bt = Backtest(GOOG, RsiOscillator, cash = 10_000)
#bt = Backtest(GOOG, SMA_MovingAverage, cash = 10_000)
bt = Backtest(GOOG, Combination, cash = 10_000)


stats = bt.run()
bt.plot()
print(stats)

#stats = bt.run()
# stats = bt.optimize(
#         upper_bound = range(55,85, 1),
#         lower_bound = range(10,45, 1),
#         rsi_window = range(10,30, 1),
#         maximize = optim_func,
#         constraint = lambda param: param.upper_bound > param.lower_bound,
#         max_tries = 100)

#print(stats)
# upper_bound = stats['_strategy'].upper_bound
# bt.plot(filename=f"plots/plot{upper_bound}.html")



# stats, heatmap = bt.optimize(
#         upper_bound = range(55,85, 5),
#         lower_bound = range(10,45, 5),
#         rsi_window = range(10, 45, 5),#14,
#         maximize = 'Sharpe Ratio',#optim_func,
#         constraint = lambda param: param.upper_bound > param.lower_bound,
#         return_heatmap = True)

# print(heatmap)



# hm = heatmap.groupby(['upper_bound','lower_bound']).mean().unstack()

# sns.heatmap(hm, cmap='viridis')
# plt.show()

# print(hm)


# displays heatmap
#plot_heatmaps(heatmap, agg="mean")

# stats = bt.run()
# bt.plot()
# print(stats)




