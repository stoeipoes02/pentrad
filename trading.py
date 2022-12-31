import time
import bybit

client = bybit.bybit(test=False, api_key="./config.api_key", api_secret="./config.api_secret")
print("loggedin")