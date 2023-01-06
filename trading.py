import requests
#import sys
import bybit
import datetime
from pybit import inverse_perpetual
#webrequest contract modules
import hmac
import uuid
import hashlib
import time

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

api_key='Y30aFoxzTGQaCTybPC'
secret_key='WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc'
httpClient=requests.Session()
recv_window=str(5000)
url="https://api-testnet.bybit.com" # Testnet endpoint

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(params)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if(method=="POST"):
        response = httpClient.request(method, url+endpoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endpoint+"?"+payload, headers=headers)
    print(response.text)
    print(Info + " Elapsed Time : " + str(response.elapsed))

def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature

#Create Order
endpoint="/contract/v3/private/order/create"
method="POST"
orderLinkId=uuid.uuid4().hex
params='{"symbol": "BTCUSDT","side": "Buy","positionIdx": 1,"orderType": "Limit","qty": "0.001","price": "20000","timeInForce": "GoodTillCancel","orderLinkId": "' + orderLinkId + '"}'
HTTP_Request(endpoint,method,params,"Create")






# #Exponential Moving Average     EMA 12-26H
# def timedelta(symbol="ETHUSDT",candles=24, timeframe=3600, interval=60):
#     now = datetime.datetime.utcnow()
#     enddate = int(now.timestamp() + 3600)
#     startdate = enddate - (timeframe * candles)

#     # difference in price price on derivatives chart without mark-price gives numbers as given on bybit platform
#     link2 = f'https://api-testnet.bybit.com/derivatives/v3/public/mark-price-kline?category=linear&symbol=ETHUSDT&interval={interval}&start={startdate*1000}&end={enddate*1000}'
#     link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={startdate * 1000}&end={enddate * 1000}'
    
#     print(link)
#     response = requests.get(link)
#     data = response.json()
#     return data

# #simple moving average 12 and 26 but need double the data because moving average is lagging
# def simplemovingaverage(symbol="ETHUST",interval=24, candle=3600, timeframe=60):
#     simplemovingaveragelist = []
#     data = timedelta(symbol, interval, candle, timeframe)['result']['list']
#     firstloop = 0
#     secondloop = int(interval / 2)
#     for i in range(firstloop, secondloop):
#         sum = 0
#         for j in range(firstloop,secondloop):
#             sum += float(data[j][4])
#         simplemovingaveragelist.append(round(sum / (interval / 2),3))
#         firstloop += 1
#         secondloop += 1
#     return simplemovingaveragelist

# slowmovingaverage = simplemovingaverage("BTCUSDT",52)
# fastmovingaverage = simplemovingaverage("BTCUSDT",24)

# print('fast',fastmovingaverage)
# print('slow',slowmovingaverage[:12])
