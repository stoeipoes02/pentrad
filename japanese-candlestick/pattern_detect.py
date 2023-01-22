import talib
import yfinance as yf
import sys
sys.path.insert(0, 'C:/Users/31680/Desktop/pentrad')
from trading import timedelta

data = yf.download("BTC", start="2022-11-01", end="2023-01-22")

engulfing = talib._ta_lib.CDLINVERTEDHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
#print(engulfing)
print(engulfing[engulfing != 0])

#print(talib.get_functions())

data = timedelta(symbol="BTCUSDT", candles=200, timeframe=3600, interval=60)['result']['list']

dataframe = []

for i in range(len(data)):
    dataframe.append(data[i][:5])

import pandas as pd
df = pd.DataFrame(dataframe, columns=['time', 'open','high', 'low','close'])

hammer = talib._ta_lib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])

df['hammer'] = hammer

hammer_days = df[df['hammer'] != 0]

print(hammer_days)