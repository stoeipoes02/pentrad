import time
import bybit
import sys

sys.path.append("../")
import creds

client = bybit.bybit(test=False, api_key="MYb1xx5hLrv6UqET1x", api_secret=creds.api_secret)
print("does this work?", creds.api_secret)
print("loggedin")