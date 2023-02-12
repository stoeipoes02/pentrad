import requests
import time
import talib
import numpy as np

# Issues:
# getdata link v3 instead of v5

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

#value = SMA(getdata(), 2)
#print(value)


# list comprehension
word = getdata(startend=3600)
empty = [(x[1:5]) for x in word]
floaters = np.array([[float(x) for x in inner]for inner in empty])

one = np.array(floaters[0][0])
two = np.array(floaters[0][1])
three = np.array(floaters[0][2])
four = np.array(floaters[0][3])

#integer = talib.CDLHAMMER(one,two,three,four)
