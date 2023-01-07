import requests
#import sys
import bybit
import datetime
from pybit import inverse_perpetual

#raspberry pi
#sys.path.append("../")
#import creds

#session_auth = inverse_perpetual.HTTP(
#    endpoint="https://api.bybit.com",
#    api_key="vzgFHwAsjwMBhlRgtb",
#    api_secret=creds.api_secret
#)

#testnet_session_auth
from pybit import inverse_perpetual
session = inverse_perpetual.HTTP(
    endpoint='https://testnet.bybit.com',
    api_key="Y30aFoxzTGQaCTybPC",
    api_secret="WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc"
)

from pybit import usdt_perpetual
session_auth = usdt_perpetual.HTTP(
    endpoint="https://api-testnet.bybit.com",
    api_key="Y30aFoxzTGQaCTybPC",
    api_secret="WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc"
)
print(session_auth.place_active_order(
    symbol="BTCUSDT",
    side="Sell",
    order_type="Limit",
    qty=0.02,
    price=16941,
    time_in_force="GoodTillCancel",
    reduce_only=False,
    close_on_trigger=False,
    position_idx=0
))


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
