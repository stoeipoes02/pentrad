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
    now = datetime.datetime.utcnow()
    enddate = int(now.timestamp() + 3600)

    startdate = enddate - (timeframe * candles)

    link2 = f'https://api-testnet.bybit.com/derivatives/v3/public/mark-price-kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate*1000}&end={enddate*1000}'
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate * 1000}&end={enddate * 1000}'
    response1 = requests.get(link)
    data = response1.json()
    allprices = data['result']['list']

    return data

fastmovingaverage = timedelta(10, 3600, 60)
slowmovingaverage = timedelta(26, 3600, 60)

data = [['1672945200000', '1251.45', '1253.25', '1251.1', '1253.15', '253624.61', '317552339.645'], ['1672941600000', '1247.35', '1251.8', '1247.05', '1251.45', '439189.4', '548989992.687'], ['1672938000000', '1248.8', '1250.25', '1247.1', '1247.35', '383188.76', '478409591.1825'], ['1672934400000', '1249.3', '1250.5', '1247.25', '1248.8', '484763.71', '605324857.9415'], ['1672930800000', '1248.6', '1252.8', '1248', '1249.3', '844254.47', '1055527564.093'], ['1672927200000', '1247.35', '1250.8', '1243.15', '1248.6', '891360.53', '1111975138.297'], ['1672923600000', '1252.85', '1253.35', '1247.35', '1247.35', '724148.83', '905940094.0345'], ['1672920000000', '1255.3', '1255.55', '1251.6', '1252.85', '294517.68', '369128733.4845'], ['1672916400000', '1251.5', '1255.5', '1250.8', '1255.3', '273513.89', '342671541.31'], ['1672912800000', '1249.1', '1252.8', '1248.8', '1251.5', '348763.6', '436295386.3855']]

#print(fastmovingaverage['result']['list'])


timeline = len(data)-5
for i in range(timeline,len(data)):
    sum = 0
    for j in range(timeline, len(data)):
        number = data[i][4]
        newnumber = float(number)
        sum += newnumber
        #print(number)
    #print(i)


data = [['1672945200000', '1251.45', '1253.25', '1251.1', '1253.35', '253624.61', '317552339.645'], ['1672941600000', '1247.35', '1251.8', '1247.05', '1251.45', '439189.4', '548989992.687'], ['1672938000000', '1248.8', '1250.25', '1247.1', '1247.35', '383188.76', '478409591.1825'], ['1672934400000', '1249.3', '1250.5', '1247.25', '1248.8', '484763.71', '605324857.9415'], ['1672930800000', '1248.6', '1252.8', '1248', '1249.3', '844254.47', '1055527564.093'], ['1672927200000', '1247.35', '1250.8', '1243.15', '1248.6', '891360.53', '1111975138.297'], ['1672923600000', '1252.85', '1253.35', '1247.35', '1247.35', '724148.83', '905940094.0345'], ['1672920000000', '1255.3', '1255.55', '1251.6', '1252.85', '294517.68', '369128733.4845'], ['1672916400000', '1251.5', '1255.5', '1250.8', '1255.3', '273513.89', '342671541.31'], ['1672912800000', '1249.1', '1252.8', '1248.8', '1251.5', '348763.6', '436295386.3855']]

print(data)

firstloop = 0
secondloop = 5
for i in range(0,5):
    sum = 0
    print(data[i][0])
    for j in range(firstloop,secondloop):
        sum += float(data[j][4])

    print(sum / 5)
    print('----')
    firstloop += 1
    secondloop += 1
# for i in range(0,5):
#     print(i)
# for count, element in enumerate(data):
#     print(element[4])




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
