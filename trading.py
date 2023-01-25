import requests
#import sys
import bybit
import datetime
import time

# raspberry pi
# sys.path.append("../")
#import creds

# session_auth = inverse_perpetual.HTTP(
#    endpoint="https://api.bybit.com",
#    api_key="vzgFHwAsjwMBhlRgtb",
#    api_secret=creds.api_secret
# )

# https://github.com/bybit-exchange/api-usage-examples/blob/master/V3_demo/api_demo/contract/Encryption.py
# Credentials needed for api calls
from pybit import usdt_perpetual
session_auth = usdt_perpetual.HTTP(
    endpoint="https://api-testnet.bybit.com",
    api_key="Y30aFoxzTGQaCTybPC",
    api_secret="WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc"
)

# Enters trade with short or long based on input
# symbol: coin
# side: side of market buy/sell
# order_type: market=current price, limit=givenprice
# qty: amount to buy
# price: needed for order_type=limit to set buy/sell price
# leverage: set leverage for trade


def makeorder(symbol="ETHUSDT", side="Buy", order_type="Market", qty=1, price=10000, leverage=5):
    try:
        session_auth.set_leverage(
            symbol=symbol,
            buy_leverage=leverage,
            sell_leverage=leverage
        )
    except Exception:
        session_auth.place_active_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            qty=qty,
            price=price,
            time_in_force="GoodTillCancel",
            reduce_only=False,              #
            close_on_trigger=False,         #
            position_idx=0                  #
        )
    return None

# Returns candles with {time, open, high, low, close, volume, turnover} in json format
# symbol: coin
# candle: amount of candles to be returned
# timeframe: seconds for a single candle
# interval: intervening time between output data 1=1min 60=1h


def timedelta(symbol="ETHUSDT", candles=1, timeframe=3600, interval=60):
    now = datetime.datetime.utcnow()
    enddate = int(now.timestamp() + 3600)
    startdate = enddate - (timeframe * candles)

    link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol={symbol}&interval={interval}&start={startdate * 1000}&end={enddate * 1000}'

    response = requests.get(link)
    data = response.json()
    return data

# Returns the simple moving average for given interval,candle and timeframe
# symbol: coin
# candle: amount of seconds for a single candle
# timeframe: seconds for a single candle
# interval: intervening time between output data 1=1min, 60=1h


def simplemovingaverage(symbol="ETHUSDT", interval=12, candle=3600, timeframe=60):
    simplemovingaveragelist = []
    data = timedelta(symbol, interval*2, candle, timeframe)['result']['list']
    firstloop = 0
    secondloop = int(interval*2 / 2)
    for i in range(firstloop, secondloop):
        sum = 0
        for j in range(firstloop, secondloop):
            sum += float(data[j][4])
        simplemovingaveragelist.append(round(sum / (interval*2 / 2), 3))
        firstloop += 1
        secondloop += 1
    return simplemovingaveragelist

# Automatically longs/shorts based on simple moving average
# symbol: coin
# qty: amount to be bought of x coin
# leverage: leverage to be used for the trade
# slowinterval: slow moving average
# fastinterval: fast moving average
# candle: amount of seconds for a single candle
# timeframe: intervening time between output data 1=1min, 60=1h


def trading(symbol="ETHUSDT", qty=0.01, leverage=5, slowinterval=26, fastinterval=12, candle=60, timeframe=1):
    slowmovingaverage = simplemovingaverage(
        symbol, slowinterval, candle, timeframe)
    fastmovingaverage = simplemovingaverage(
        symbol, fastinterval, candle, timeframe)

    currentposition = session_auth.my_position(symbol=symbol)

    if fastmovingaverage[0] > slowmovingaverage[0]:
        print(fastmovingaverage[0], "long 🟢")
        if currentposition['result'][0]['side'] == "Sell":
            makeorder(side="Buy", order_type="Market",
                      qty=qty*2, leverage=leverage)
        elif currentposition['result'][0]['side'] == "None":
            makeorder(side="Buy", order_type="Market",
                      qty=qty, leverage=leverage)

    elif fastmovingaverage[0] < slowmovingaverage[0]:
        print(slowmovingaverage[0], "short 🔴")
        if currentposition['result'][0]['side'] == "Buy":
            makeorder(side="Sell", order_type="Market",
                      qty=qty*2, leverage=leverage)
        elif currentposition['result'][0]['side'] == "None":
            makeorder(side="Sell", order_type="Market",
                      qty=qty, leverage=leverage)
    print('---')


if __name__ == "__main__":
    while True:
        trading(symbol="ETHUSDT", qty=1, leverage=5, slowinterval=26,
                fastinterval=12, candle=60, timeframe=1)
        time.sleep(60)
