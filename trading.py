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

def timedelta(candles=10, timeframe=3600, interval=60):
    now = datetime.datetime.now()
    enddate = int(now.timestamp())

    startdate = enddate - (timeframe * candles)

    link2 = f'https://api-testnet.bybit.com/derivatives/v3/public/mark-price-kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate*1000}&end={enddate*1000}'
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate * 1000}&end={enddate * 1000}'
    response1 = requests.get(link)
    data = response1.json()
    allprices = data['result']['list']

    return data

fastmovingaverage = timedelta(12, 3600, 60)
slowmovingaverage = timedelta(26, 3600, 60)





def printbtcpricedaysago():
    response1 = requests.get('https://api-testnet.bybit.com/derivatives/v3/public/mark-price-kline?category=linear&symbol=ETHUSDT&interval=60&start=1672261200000&end=1672354800000')
    #response2 = requests.get('https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=ETHUSDT&interval=60&start=1672261200000&end=1672354800000')
    data = response1.json()
    allprices = data['result']['list']
    return allprices

listofprices26 = printbtcpricedaysago()
newlist = []

for i in range(len(listofprices26)):
    newlist.append(listofprices26[i][4])
    #newlist.append(listofprices26[i][0])

#print(newlist)
