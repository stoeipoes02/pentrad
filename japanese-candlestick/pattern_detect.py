import talib
import yfinance as yf
import sys
import pandas as pd
#sys.path.insert(0, 'C:/Users/31680/Desktop/pentrad')
#from trading import timedelta

data = yf.download("BTC-USD", start="2022-12-20", end="2023-01-22")

engulfing = talib._ta_lib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
#print(engulfing[engulfing != 0])
data['engulfing'] = engulfing
print(data)
#print(talib.get_functions())

# data = timedelta(symbol="BTCUSDT", candles=200, timeframe=3600, interval=60)['result']['list']
# dataframe = []
# for i in range(len(data)):
#     dataframe.append(data[i][:5])
# import pandas as pd
# df = pd.DataFrame(dataframe, columns=['time', 'open','high', 'low','close'])
# hammer = talib._ta_lib.CDLDOJI(df['open'], df['high'], df['low'], df['close'])
# df['hammer'] = hammer
# hammer_days = df[df['hammer'] != 0]
# print(hammer_days)

import requests
symbol = "BTCUSDT"
interval = "D"

startdate = 1671577200
enddate = 1674259200
data = requests.get(f"https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={startdate * 1000}&end={enddate * 1000}")
response= data.json()['result']['list']

frame = pd.DataFrame.from_records(response, columns=['time','open','high','low','close','volume','turnover'])

doji = talib.CDLDOJI(frame['open'],frame['high'],frame['low'],frame['close'])
frame['doji'] = doji

#print(frame[doji!=0])

print(frame)