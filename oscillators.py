import requests
import time
import talib
import numpy as np
import pandas as pd
import logging 

'''
Issues:
1. getdata link v3 instead of v5
2. list comprehension usage not in script
3. talib EMA doesn't have the same results as the bybit EMA but SMA and WMA do
4. talib RSI doesn't have exact result as bybit but is close
5. weights on point system dont do anything really
'''



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
data = dataframefill(3600*20)

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
        fastmoving = data['SMA5'].iloc[0]
        slowmoving = data['SMA20'].iloc[0]
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

# set up buy or sell thingy

def position(interval=1,symbol='BTCUSDT'):

    # possible with post python request
    return None

# functions to be called
if __name__ == "__main__":





    #moving_average('SMA',5)
    #moving_average('SMA',20)
    #rsi(5)

    #print(data.head(3))
    #print(point())

    position()
    #del data

import hmac
import hashlib
import json

secret = "WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc"

def get_signature(param_str):
    return str(hmac.new(bytes(secret, "utf-8"), bytes(param_str, "utf-8"), digestmod="sha256").hexdigest())

url = "https://api-testnet.bybit.com"

api_key = "Y30aFoxzTGQaCTybPC"
leverage = 1
order_type = "Limit"#market
price = 25000
qty = 1
side = "Buy"
stop_loss = 22000
symbol = "BTCUSDT"
take_profit = 26000
time_in_force = "GoodTillCancel"

def place_active_order(symbol, side, qty, price, stop_loss, take_profit, order_type="Limit",time_in_force='GoodTillCancel'):
    timestamp = int(time.time() * 1000)
    param_str = f"api_key={api_key}&leverage={leverage}&order_type={order_type}&price={price}&qty={qty}&side={side}&stop_loss={stop_loss}&symbol={symbol}&take_profit={take_profit}&time_in_force={time_in_force}&timestamp={timestamp}"
    sign = get_signature(param_str)
    data = {
        "api_key": api_key,
        "leverage": leverage,
        "timestamp": timestamp,

        "side": side,
        "symbol": symbol,
        "order_type": order_type,
        "qty": qty,
        "price": price,
        "time_in_force": time_in_force,
        "take_profit": take_profit,
        "stop_loss": stop_loss,
        "sign": sign
    }
    r = requests.post(url + "/contract/v3/private/order/create", data)
    print(r.text)

place_active_order(symbol, side, qty, price, stop_loss, take_profit, order_type, time_in_force)