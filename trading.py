import time
import bybit
import sys

sys.path.append("../")
import creds

client = bybit.bybit(test=False, api_key="vzgFHwAsjwMBhlRgtb", api_secret=creds.api_secret)

print("loggedin")