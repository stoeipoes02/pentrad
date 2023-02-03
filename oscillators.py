import requests
import time
import talib
import numpy

# Returns current time in milliseconds and the time of x seconds ago since epoch
def timedelta(times=3600):
    millisecnow = round(time.time() * 1000)
    starttime = millisecnow - times * 1000
    return millisecnow, starttime

startend = timedelta(times=86400*2)

link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=BTCUSDT&interval=D&start={startend[1]}&end={startend[0]}'

r = requests.get(link).json()
data = r['result']['list']
print(data)


## work in progress numpyndarray??? 

closes = []
for count, value in enumerate(data):
    print(count, value)
    closes.append(value[4])

print(closes)

test = [23435, 23493.5]
blup = numpy.array(test)


print(talib.SMA(numpy, 2))