import requests
import time
import talib
import numpy as np
import pandas as pd
import logging 
import hmac
import hashlib
import uuid
import json

from pentrad.apikeys import API_KEY, SECRET_KEY

'''
Issues:
1. script is v3 instead of v5
2. list comprehension usage not in script
3. talib EMA doesn't have the same results as the bybit EMA but SMA and WMA do
4. talib RSI doesn't have exact result as bybit but is close
5. weights on point system dont do anything really
6. using pandas dataframe but has problems like importing 
'''

# https://bybit-exchange.github.io/docs/derivatives/contract/place-order
httpClient=requests.Session()
recv_window=str(5000)
url="https://api-testnet.bybit.com"

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': API_KEY,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    #print(response.text)
    #print(Info + " Elapsed Time : " + str(response.elapsed))

    return response.text

def genSignature(payload):
    param_str= str(time_stamp) + API_KEY + recv_window + payload
    hash = hmac.new(bytes(SECRET_KEY, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature








# Returns current time in milliseconds and the time of x seconds ago since epoch
def timedelta(times=3600):
    millisecnow = round(time.time() * 1000)
    starttime = millisecnow - times * 1000
    return millisecnow, starttime


# Gets the data of bybit api
# symbol: coin to be traded
# interval: timeframe of candles 1,3,5,15,30,60,120,240,360,720,D,W,M
# startend: start of time until current time in seconds
def getdata(symbol="BTCUSDT", interval=60,starttime=3600):
    starttime = timedelta(starttime)
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={starttime[1]}&end={starttime[0]}'
    r = requests.get(link).json()
    data = r['result']['list']
    return data



# Transforms the given list into either a list of lists or a numpy array
# data: the source of the data
# element: element of the list to be chosen
# types: boolean for numpy array or list of lists
def transform(data:list, element:int, types:bool):
    # below comment might help with choosing multiple elements of a list
    #list = [(x[element[0]],x[element[1]]) for x in data]

    list = [x[element] for x in data]
    if types:
        float_list = [float(x) for x in list[::-1]]
        result = np.array(float_list)
    else:
        result = [[i] for i in list]

    return result


# returns the last slow and fast moving average values in a list
def pointsmovingaverage(symbol, interval, starttime, item, slowmoving, fastmoving):
    data = getdata(symbol,interval,starttime)
    transformed_data = transform(data,item,True)

    slow = talib.WMA(transformed_data,slowmoving)
    fast = talib.WMA(transformed_data,fastmoving)

    return slow,fast








def create_order(symbol, side, orderType, qty, price):
    endpoint="/contract/v3/private/order/create"
    method="POST"
    orderLinkId=uuid.uuid4().hex
    params={"symbol": symbol,"side": side,"positionIdx": 0,"orderType": orderType,"qty": qty,"price": price,"timeInForce": "GoodTillCancel","orderLinkId": orderLinkId}
    newparams = json.dumps(params)
    params = newparams.replace('\\','')
    
    return HTTP_Request(endpoint,method,params,"Create")



def get_open_positions(symbol):
    endpoint = "/contract/v3/private/position/list"
    method = "GET"
    params=f'symbol={symbol}'
    position = json.loads(HTTP_Request(endpoint,method, params, 'filled orders'))
    
    return position['result']['list'][0]


if __name__ == "__main__":
    # while True:
    #     side = get_open_positions("BTCUSDT")

    #     if side == 'None':
    #         pass
    #     else:
    #         slow,fast = pointsmovingaverage("BTCUSDT",15,7200,4,6,3)

    #         if side == "Buy":
    #             if fast[-1] >= slow[-1]:
    #                 print('fast above slow')
    #             else:
    #                 print('slow above fast')
     
    #         elif side == "Sell":
    #             if fast[-1] <= slow[-1]:
    #                 print('fast under slow')
    #             else:
    #                 print('slow under fast')

    #     time.sleep(60)

    #print(get_open_positions("BTCUSDT"))
    print(create_order("BTCUSDT","Buy","Limit","0.01","10000"))

    pass



#Get filled orders
# endpoint = "/contract/v3/private/position/list"
# method = "GET"
# params='symbol=BTCUSDT'
# print(HTTP_Request(endpoint,method, params, 'filled orders'))

#Get unfilled orders
# endpoint = "/contract/v3/private/order/unfilled-orders"
# method = "GET"
# params="symbol=BTCUSDT"
# HTTP_Request(endpoint,method,params, 'unfilled orders')

#Cancel unfilled order
# endpoint = "/contract/v3/private/order/cancel"
# method = "POST"
# params='{"symbol":"BTCUSDT","orderLinkId":"66c178973bd245649ceb7cbb565509fa"}'
# HTTP_Request(endpoint,method,params, 'cancel certain order')

#Setting leverage
# endpoint = "/contract/v3/private/position/set-leverage"
# method = "POST"
# params = '{"symbol":"BTCUSDT","buyLeverage":"20","sellLeverage":"20"}'
# HTTP_Request(endpoint,method,params,'setting leverage')
