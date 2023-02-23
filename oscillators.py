import requests
import time
import talib
import numpy as np
import pandas as pd
import logging 


prvkey = '''-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCTbm2XPyPLZtJ6
eRm/w/sB/Ibnl1eo6Pn+FqdItE23APFV9sCJCXScR3zjyWdlSzMd16ucJHgWxibN
mBZnQrwq2rF6+TQ6GCBclbigG+hlQsZtiansKQHzQseYtOYTMbvZ8tpDloCVB6R3
OPrsdeoKZxkHaOPQgHAVzFuepCXzMA+BJjCMV+mT8p039SLuyeultZ4kU1p2Et9j
wBsHkILoJ5mYuk9/+JSwW6wWst1IQiPzFipqCuS7ruWekCZ4DX5jI+urtY9rAaQY
YpVkiRJViAVKxXtOvDFNgdC9Jp6fDJHyFXOccIgRD/6W5HmxnsTb7dApKjHRx13r
7IV1JQ01AgMBAAECggEAGjYKRtcDYqCrr/mCweyyXhaK13a5L38IHwvg/tSLcos4
3NsrPNHRCQ3OnuLKPqCBfH9A89gp/4aIFIpDBWXAdW//GMlgZymt6zf1JIYBqasX
Axdz/dgGkDyhpr0WoHf5mVSLSHPj9Vrv+wBG4C5QhzvwH7ietA15n+5+pXQyiQsP
xZhgIYQMvwGSXHw7Gie2DadAncMUMxIdM2raHU+8o2KM5ktZBIPokj3bFLxSRafy
OQZfemHqoyHs/ecjbX3gLPi0uFFNKUQhd9SVK6LzwROeKSjqGXWhv/Qh5zz9xJlb
RiYPhohehat4zUfD5mF1NQDAUdjl7ge1GoW6hgIKKwKBgQDG1MYaeEFTGXZI975Q
Ar210bVUUQA2NAfqt3a75BxNFezOJeFA3cioqT7dtbVd+tx66lIrNMaIJami1hGu
14KQYWs/2+WyNdKFmRorXqNm0yJqxFKPP6vxoajjzOok27L+Ad4RrFGb5KQFRpBC
w/cy+Wu8betgHEhOcfyFypGCMwKBgQC90k5GACJb1eQJgLhgYGbFmeFH4XWHGqby
ZfR2XqMhnaXdvkU0YioCgFHIfQ+UX5h7m+Um1sJg2O7hV/yLA5gb4BuSP1xDDgZK
hI4Nc99VZxmneKNipwByWLL5GjnWxCCNyUaPnVAVGCzckdMExn5fHBXLeeto2hkC
4bOCp5va9wKBgDJygeDtagWfjDdvREYgq+mZz5wZASi/gtK2wdViRxv32CFl0wUW
QHcqmdy+4cl6gL5e/YIg3c5lX+kEz2/BFktzrDaDoH/a0BM9iTo/xM2t/CmCrj/S
M9oW3jcOIso/Q+bWqnVpdztKg6MjCC8ocWvphMBGU1YLVv0wRpXbk5epAoGAUESb
JsytusnSuRX+YXrCWrK8acn0CeKCUCQ+4MMaFn/0gLURzJnqC865Rp9jtClMcJC2
sNrFrXBua0nql9o4OylkX059tDk8/cvZyeSCvzluxruj03atIK1TWTT22lNrNKm1
'''
pubkey = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk25tlz8jy2bSenkZv8P7
AfyG55dXqOj5/hanSLRNtwDxVfbAiQl0nEd848lnZUszHdernCR4FsYmzZgWZ0K8
Ktqxevk0OhggXJW4oBvoZULGbYmp7CkB80LHmLTmEzG72fLaQ5aAlQekdzj67HXq
CmcZB2jj0IBwFcxbnqQl8zAPgSYwjFfpk/KdN/Ui7snrpbWeJFNadhLfY8AbB5CC
6CeZmLpPf/iUsFusFrLdSEIj8xYqagrku67lnpAmeA1+YyPrq7WPawGkGGKVZIkS
VYgFSsV7TrwxTYHQvSaenwyR8hVznHCIEQ/+luR5sZ7E2+3QKSox0cdd6+yFdSUN
NQIDAQAB
-----END PUBLIC KEY-----
'''

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
import uuid

api_key='Y30aFoxzTGQaCTybPC'
secret_key='WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc'
httpClient=requests.Session()
recv_window=str(5000)
url="https://api-testnet.bybit.com" # Testnet endpoint

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
params='{"symbol": "BTCUSDT","side": "Buy","positionIdx": 0,"orderType": "Limit","qty": "0.001","price": "10000","timeInForce": "GoodTillCancel","orderLinkId": "' + orderLinkId + '"}'
HTTP_Request(endpoint,method,params,"Create")