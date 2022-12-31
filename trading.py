import bybit
import time
import config

client = bybit.bybit(test=False, api_key=config.api_key, api_secret=config.api_secret)
print("loggedin")