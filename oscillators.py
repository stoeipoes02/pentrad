import requests
import time
import talib
import numpy as np
import pandas as pd

# Issues:
# getdata link v3 instead of v5
# list comprehension usage not in script

# Returns current time in milliseconds and the time of x seconds ago since epoch
def timedelta(times=3600):
    millisecnow = round(time.time() * 1000)
    starttime = millisecnow - times * 1000
    return millisecnow, starttime


# Gets the data of bybit api
# symbol: coin to be traded
# interval: timeframe of candles 1,3,5,15,30,60,120,240,360,720,D,W,M
# startend: start of time until current time in seconds
def getdata(symbol="BTCUSDT", interval=15,startend=3600):
    startend = timedelta(startend)
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={startend[1]}&end={startend[0]}'
    r = requests.get(link).json()
    data = r['result']['list']
    return data


# Simple Moving Average that takes data and turns it into a moving average
# data: data of price from kline request
# length: moving average length which will be returned
# length-1 removes all the nan values
def SMA(data, length):
    closes = []
    for count, value in enumerate(data):
        closes.append(float(value[4]))
    
    arr = np.array(closes)
    simple_MA = talib.SMA(arr, length)
    return simple_MA[length-1:]


# creates dataframe with columns: time, open, high, low, close, volume and turnover
# uses list comprehension to fill the right value to every row/column
def dataframefill(startend):
    blub = getdata(startend=startend)
    data = pd.DataFrame(columns=['Time','Open','High','Low','Close','Volume', 'Turnover'])

    i = 0
    for col in data.columns:
        data[f'{col}'] = [(x[i])for x in blub]
        i += 1
    return data

cum = dataframefill(3600)
print(cum)

sma = talib.SMA(cum['Close'],2)
print(sma[1:])