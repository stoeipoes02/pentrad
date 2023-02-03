import requests
import time


#def timedelta(symbol="ETHUSDT", timeframe=60)
millisecnow = round(time.time() * 1000)
starttime = millisecnow - 86400 * 1000 * 2

link = f'https://api-testnet.bybit.com/derivatives/v3/public/kline?category=linear&symbol=BTCUSDT&interval=60&start={starttime}&end={millisecnow}'

r = requests.get(link)
print(r.json())






# def timedelta(symbol="ETHUSDT", candles=1, timeframe=3600, interval=60):


#     response = requests.get(link)
#     data = response.json()
#     return data