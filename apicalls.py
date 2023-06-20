from pybit.unified_trading import HTTP
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
import mplfinance as mpf

from apikeys import API_KEY, API_SECRET



'''
Issues:
1. script is v3 instead of v5
2. list comprehension usage not in script
3. talib EMA doesn't have the same results as the bybit EMA but SMA and WMA do
4. talib RSI doesn't have exact result as bybit but is close
'''


# -----------------SESSION CREATION---------------------#
session = HTTP(
    testnet=True,
    api_key=API_KEY,
    api_secret=API_SECRET,
)


# ----------------MAIN CODE-------------------------------#





# Returns current time in milliseconds and the time of x seconds ago since epoch
def timedelta(times=3600):
    millisecnow = round(time.time() * 1000)
    starttime = millisecnow - times * 1000
    return millisecnow, starttime


# Gets the data of bybit api
# symbol: coin to be traded
# interval: timeframe of candles 1,3,5,15,30,60,120,240,360,720,D,W,M
def getdata(symbol="BTCUSDT", interval=60, starttime=36000):
    endtime, starttime = timedelta(starttime)
    data = session.get_kline(category="spot",
                             symbol=symbol,
                             interval=interval,
                             start=starttime,
                             end=endtime)
    try: 
        if data['retCode'] == 0:
            return data['result']['list']
        
    except Exception as e:
        return e




def entryprice(symbol="BTC"):
    symbol = f'{symbol}USDT'
    tickers = session.get_tickers(category="spot", symbol=symbol)
    entryprice = tickers['result']['list'][0]['lastPrice']
    return entryprice



# Transforms the given list into either a list of lists or a numpy array
# data: the source of the data
# element: element of the list to be chosen
# types: boolean for numpy array or list of lists
def transform(data: list, element: int, types: bool):
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
def pointsmovingaverage(symbol, interval, starttime, element, slowmoving, fastmoving):
    data = getdata(symbol, interval, starttime)
    transformed_data = transform(data, element, True)

    slow = talib.SMA(transformed_data, slowmoving)
    fast = talib.SMA(transformed_data, fastmoving)

    return slow, fast


# def create_order(symbol="BTCUSDT", side="Buy", orderType="Limit", qty="0.01", price="10000"):
#     endpoint="/contract/v3/private/order/create"
#     method="POST"
#     #orderLinkId = f'{symbol};{side};{orderType};{qty};{price}'
#     orderLinkId=uuid.uuid4().hex
#     params={"symbol": symbol,"side": side,"positionIdx": 0,"orderType": orderType,"qty": qty,"price": price,"timeInForce": "GoodTillCancel","orderLinkId": orderLinkId}
#     newparams = json.dumps(params)
#     params = newparams.replace('\\','')

#     return HTTP_Request(endpoint,method,params,"Create")


# def set_take_profit():
#     endpoint = "/contract/v3/private/position/trading-stop"
#     method = "POST"
#     params={"symbol": "BNBUSDT","takeProfit": "400","stopLoss": "300","positionIdx": 0}
#     newparams = json.dumps(params)
#     params = newparams.replace('\\','')

#     return HTTP_Request(endpoint,method,params,"set take profit")



# Get filled orders
print(session.get_positions(
    category="inverse",
    symbol="BTCUSDT",
))


print(session.set_leverage(
    category="inverse",
    symbol="BTCUSDT",
    buyLeverage="6",
    sellLeverage="6",
))


# place order
print(session.place_order(
    category="inverse",
    symbol="BTCUSDT",
    side="Buy",
    orderType="Market",
    qty="0.01",
    price="26000",
    timeInForce="GTC",
    orderLinkId=None,
    isLeverage=0,
    orderFilter="Order",
))

# Get unfilled orders
# endpoint = "/contract/v3/private/order/unfilled-orders"
# method = "GET"
# params="symbol=BTCUSDT"
# HTTP_Request(endpoint,method,params, 'unfilled orders')

# Cancel unfilled order
# endpoint = "/contract/v3/private/order/cancel"
# method = "POST"
# params='{"symbol":"BTCUSDT","orderLinkId":"66c178973bd245649ceb7cbb565509fa"}'
# HTTP_Request(endpoint,method,params, 'cancel certain order')

# Setting leverage
# endpoint = "/contract/v3/private/position/set-leverage"
# method = "POST"
# params = '{"symbol":"BTCUSDT","buyLeverage":"20","sellLeverage":"20"}'
# HTTP_Request(endpoint,method,params,'setting leverage')
