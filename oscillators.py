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
import csv

import mplfinance as mpf

from pentrad.apikeys import API_KEY, SECRET_KEY

'''
Issues:
1. script is v3 instead of v5
2. list comprehension usage not in script
3. talib EMA doesn't have the same results as the bybit EMA but SMA and WMA do
4. talib RSI doesn't have exact result as bybit but is close
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

    return response.text

def genSignature(payload):
    param_str = str(time_stamp) + API_KEY + recv_window + payload
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
def getdata(symbol="BTCUSDT", interval=60,starttime=36000):
    starttime = timedelta(starttime)
    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={starttime[1]}&end={starttime[0]}'
    r = requests.get(link).json()
    data = r['result']['list']
    return data



def getdataasgraph(symbol="BTCUSDT", interval=60, candles=10, style='yahoo', volume=True):
    if not isinstance(interval, int):
        if interval == "D":
            newinterval = 1440
        elif interval == "W":
            newinterval = 10080
        elif interval == "M":
            newinterval = 43800
    else:
        newinterval = interval 
    
    starttime = newinterval * candles * 60
    data = getdata(symbol, interval, starttime)

    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'market_cap'])

    df = df.set_index('date')
    df.index = pd.to_datetime(df.index, unit='ms')

    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)

    # https://github.com/matplotlib/mplfinance/blob/master/examples/styles.ipynb
    fig, ax = mpf.plot(df, type='candle', volume=volume, style=style, show_nontrading=True, returnfig=True)

    # Save the plot as a PNG file
    filename = f'graphs/{symbol}{interval}{candles}.png'
    
    fig.savefig(filename)
    return filename

# styles
'''
classic
charles
mike
blueskies
starsandstripes
brasil
yahoo
'''



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
def pointsmovingaverage(symbol, interval, starttime, element, slowmoving, fastmoving):
    data = getdata(symbol,interval,starttime)
    transformed_data = transform(data,element,True)

    slow = talib.SMA(transformed_data,slowmoving)
    fast = talib.SMA(transformed_data,fastmoving)

    return slow,fast








def create_order(symbol="BTCUSDT", side="Buy", orderType="Limit", qty="0.01", price="10000"):
    endpoint="/contract/v3/private/order/create"
    method="POST"
    #orderLinkId = f'{symbol};{side};{orderType};{qty};{price}'
    orderLinkId=uuid.uuid4().hex
    params={"symbol": symbol,"side": side,"positionIdx": 0,"orderType": orderType,"qty": qty,"price": price,"timeInForce": "GoodTillCancel","orderLinkId": orderLinkId}
    newparams = json.dumps(params)
    params = newparams.replace('\\','')
    
    return HTTP_Request(endpoint,method,params,"Create")


def set_take_profit():
    endpoint = "/contract/v3/private/position/trading-stop"
    method = "POST"
    params={"symbol": "BNBUSDT","takeProfit": "400","stopLoss": "300","positionIdx": 0}
    newparams = json.dumps(params)
    params = newparams.replace('\\','')
    
    return HTTP_Request(endpoint,method,params,"set take profit")




# with open('pentrad/users.csv', 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         trades = row['activetrades'].split(',')
        
#         print(f"User {row['user_id']}: {row['name']}'s trades - {trades}")





def get_open_positions(symbol="BTCUSDT"):
    endpoint = "/contract/v3/private/position/list"
    method = "GET"
    params = f'symbol={symbol}'
    position = json.loads(HTTP_Request(endpoint,method,params,'test positions'))
    return position

positions = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT"]

# for i in positions:
#     print(get_open_positions(symbol=i))



def PnL(symbol):
    endpoint = "/contract/v3/private/position/closed-pnl"
    method = "GET"
    params = f"symbol={symbol}"
    winning = json.loads(HTTP_Request(endpoint,method,params,'Profit and Loss'))
    return winning

winlist = PnL("BTCUSDT")

newwinlist = winlist['result']['list']

# for items in newwinlist:
#     print(items['closedPnl'])



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
