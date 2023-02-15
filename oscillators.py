import requests
import time
import talib
import numpy as np
import pandas as pd

'''
Issues:
1. getdata link v3 instead of v5
2. list comprehension usage not in script
3. talib EMA doesn't have the same results as the bybit EMA but SMA and WMA do
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
data = dataframefill(28800)

# moving average method SMA/WMA/EMA with the amount of candles
def moving_average(MO,candles):
    # gets the data of close and turns it into list
    closesdata = data['Close'].tolist()
    # reverses the list so sma function can use it
    reversed_closesdata = closesdata[::-1]
    # turns the list into a bunch of floats
    reversed_closesdata_float = [float(item) for item in reversed_closesdata]
    # turns the float data into a numpy array
    reversed_closesdata_floatarray = np.array(reversed_closesdata_float)
    # executes the ma function and checks whether its SMA/WMA/EMA
    method = MO.replace("'","")
    if method == "SMA":
        data[MO] = talib.SMA(reversed_closesdata_floatarray, candles)[::-1]
        return True
    elif method == "WMA":
        data[MO] = talib.WMA(reversed_closesdata_floatarray, candles)[::-1]
        return True
    elif method == "EMA":
        data[MO] = talib.EMA(reversed_closesdata_floatarray, candles)[::-1]
        return True
    else:
        return False

    maanswer = talib.WMA(reversed_closesdata_floatarray, 3)
    # reversed the array so last item becomes the first item
    reversed_maanswer = maanswer[::-1]
    # append it to dataframe
    data[MO] = reversed_maanswer


moving_average('SMA',5)
moving_average('EMA',5)
moving_average('WMA',5)
print(data)
