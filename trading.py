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
twelve = 43200
twentysix = 93600
now = 1672354800 
def printbtcpricedaysago():
    #response1 = requests.get('https://api-testnet.bybit.com/derivatives/v3/public/mark-price-kline?category=linear&symbol=ETHUSDT&interval=60&start=1672261200000&end=1672354800000')
    response2 = requests.get('https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=ETHUSDT&interval=60&start=1672261200000&end=1672354800000')
    data = response2.json()
    allprices = data['result']['list']
    return allprices

listofprices26 = printbtcpricedaysago()
newlist = []
print(listofprices26)
i = 0
for i in range(len(listofprices26)):
    newlist.append(listofprices26[i][4])
    newlist.append(listofprices26[i][0])

print(newlist)

#print(printbtcpricedaysago())

def print_btcprice():
    response = requests.get("https://api.bybit.com/derivatives/v3/public/tickers?category=linear&symbol=ETHUSDT")
    data = response.json()
    price = data['result']['list'][0]['lastPrice']
    return price
print(print_btcprice())

#for i in range(len(info['result'])):
#    print(f"{info['result'][i]['symbol']:<30} {info['result'][i]['bid_price']}")
#    if info['result'][i]['symbol'] == 'FTMUSDT':
#        print('yeeea found it', i)

#print(session_auth.place_active_order(
#    symbol="XRPUSD",
#    side="Buy",
#    order_type="Market",
#    qty=1,
#    time_in_force="GoodTillCancel"
#))