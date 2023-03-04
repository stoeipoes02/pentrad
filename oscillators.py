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
api_key='Y30aFoxzTGQaCTybPC'
secret_key='WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc'
httpClient=requests.Session()
recv_window=str(5000)
url="https://api-testnet.bybit.com"

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
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
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(secret_key, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
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

datas = getdata("BTCUSDT", 15, 3600)
blub = transform(datas,4,True)

print(talib.WMA(blub,3))









# creates dataframe with columns: time, open, high, low, close, volume and turnover
# uses list comprehension to fill the right value to every row/column
def dataframefill(starttime):
    blub = getdata(starttime=starttime)
    data = pd.DataFrame(columns=['Time','Open','High','Low','Close','Volume', 'Turnover'])

    i = 0
    for col in data.columns:
        data[f'{col}'] = [(x[i])for x in blub]
        i += 1
    return data

# create dataframe
data = dataframefill(3600*27)

# moving average method SMA/WMA/EMA with the amount of candles
def moving_average(MO,candles):
    # gets the data of close and turns it into list then reverses the list
    closesdata = data['Close'].tolist()[::-1]
    # turns the list into a bunch of floats and turns it into an array
    reversed_closesdata_floatarray = np.array([float(item) for item in closesdata])

    # executes the ma function and checks whether its SMA/WMA/EMA
    method = MO.replace("'","")
    if method == "SMA":
        data[MO+f'{candles}'] = talib.SMA(reversed_closesdata_floatarray, candles)[::-1]
        return True
    elif method == "WMA":
        data[MO+f'{candles}'] = talib.WMA(reversed_closesdata_floatarray, candles)[::-1]
        return True
    elif method == "EMA":
        data[MO+f'{candles}'] = talib.EMA(reversed_closesdata_floatarray, candles)[::-1]
        return True
    else:
        return False


# reverses output of close so rsi gets aligned right
def rsi(candles):
    dat = data['Close'].tolist()[::-1]
    dat_array = np.array([float(item) for item in dat])
    data['RSI'] = talib.RSI(dat_array,candles)[::-1]

# point system
def point():
    # configure logging file
    logging.basicConfig(filename='example.log', level=logging.WARNING)
    points = {}
    try:
        # point difference for the SMA's
        fastmoving = data['SMA12'].iloc[0]
        slowmoving = data['SMA26'].iloc[0]
        if fastmoving >= slowmoving:
            difference = (fastmoving-slowmoving) / slowmoving
            points['SMA'] = {'value':1,'weight':round(difference,4)}
        else:
            difference = (slowmoving-fastmoving) / fastmoving
            points['SMA'] = {'value':0,'weight':round(difference,4)}
    except Exception as e:
        logging.error(e)

    try:
        rsivalue = data['RSI'][0]
        if rsivalue > 50:
            points['RSI'] = {'value':0, 'weight':rsivalue/100}
        else:
            points['RSI'] = {'value':1, 'weight':rsivalue/100}
    except Exception as e:
        logging.error(e)
    return points




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
    
    return position['result']['list'][0]['side']


if __name__ == "__main__":


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
