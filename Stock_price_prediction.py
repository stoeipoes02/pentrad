# Artificial recurrent neural network called Long Short Term Memory (LSTM)
import math
import pandas_datareader as web
import numpy as numpy
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Get the stock quote
df = web.DataReader('AAPL', data_source='yahoo', start='2012-01-01', end='2019-12-17')
df
#df.shape

# visualise closing price
# plt.figure(figsize=(16,8))
# plt.title('close price history')
# plt.plot(df['Close'])
# plt.xlabel('Date', fontsize=18)
# plt.ylabel('Close Price USD ($)',  fontsize=18)
# plt.show()