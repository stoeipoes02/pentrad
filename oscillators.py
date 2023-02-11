import requests
import time
import talib
from numpy import array

# Returns current time in milliseconds and the time of x seconds ago since epoch
def timedelta(times=3600):
    millisecnow = round(time.time() * 1000)
    starttime = millisecnow - times * 1000
    return millisecnow, starttime


#  
def getdata():
    startend = timedelta(times=86400*5)
    symbol = "BTCUSDT"
    interval = "D"
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={startend[1]}&end={startend[0]}'
    r = requests.get(link).json()
    data = r['result']['list']
    return data

print(getdata())


# Simple Moving Average that takes data and turns it into a moving average
# data: data of price from kline request
# length: moving average length which will be returned
# length-1 removes all the nan values
def SMA(data, length):
    closes = []
    for count, value in enumerate(data):
        closes.append(float(value[4]))
    
    arr = array(closes)
    simple_MA = talib.SMA(arr, length)
    return simple_MA[length-1:]

value = SMA(getdata(), 2)
print(value)

# print(talib.STOCH(high, low, close))
