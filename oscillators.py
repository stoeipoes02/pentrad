import requests
import time
import talib
from numpy import array

# Returns current time in milliseconds and the time of x seconds ago since epoch
def timedelta(times=3600):
    millisecnow = round(time.time() * 1000)
    starttime = millisecnow - times * 1000
    return millisecnow, starttime

startend = timedelta(times=86400*2)

link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=BTCUSDT&interval=D&start={startend[1]}&end={startend[0]}'

r = requests.get(link).json()
data = r['result']['list']
#print(data)


## Simple Moving Average that takes data and turns it into a moving average
# 
def SMA():
    closes = []
    for count, value in enumerate(data):
        closes.append(float(value[4]))
    
    arr = array(closes)
    simpleMA = talib.SMA(arr, len(arr))

    return simpleMA[len(arr)-1]

print(SMA())