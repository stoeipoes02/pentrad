import requests
#import sys
import bybit
import time
import datetime
from pybit import inverse_perpetual
import pandas as pd
import calendar

#raspberry pi
#sys.path.append("../")
#import creds

#session_auth = inverse_perpetual.HTTP(
#    endpoint="https://api.bybit.com",
#    api_key="vzgFHwAsjwMBhlRgtb",
#    api_secret=creds.api_secret
#)

#testnet_session_auth
session = inverse_perpetual.HTTP(
    endpoint='https://testnet.bybit.com',
    api_key="Y30aFoxzTGQaCTybPC",
    api_secret="WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc"
)

#Exponential Moving Average     EMA 12-26H
def timedelta(candles=24, timeframe=3600, interval=60):
    now = datetime.datetime.utcnow()
    enddate = int(now.timestamp() + 3600)
    startdate = enddate - (timeframe * candles)

    # difference in price price on derivatives chart without mark-price gives numbers as given on bybit platform
    link2 = f'https://api-testnet.bybit.com/derivatives/v3/public/mark-price-kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate*1000}&end={enddate*1000}'
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate * 1000}&end={enddate * 1000}'
    
    response = requests.get(link)
    data = response.json()
    return data

#simple moving average 12 and 26 but need double the data because moving average is lagging
def simplemovingaverage(interval=24, candle=3600, timeframe=60):
    simplemovingaveragelist = []
    data = timedelta(interval, candle, timeframe)['result']['list']
    firstloop = 0
    secondloop = int(interval / 2)
    for i in range(firstloop, secondloop):
        sum = 0
        for j in range(firstloop,secondloop):
            sum += float(data[j][4])
        simplemovingaveragelist.append(round(sum / (interval / 2),2))
        firstloop += 1
        secondloop += 1
    return simplemovingaveragelist

bitches = simplemovingaverage(10)

print(bitches)