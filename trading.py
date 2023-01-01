import time
import sys
import bybit
from pybit import inverse_perpetual

sys.path.append("../")
import creds

session_auth = inverse_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key="vzgFHwAsjwMBhlRgtb",
    api_secret=creds.api_secret
)
print(session_auth.get_wallet_balance(coin="USDT"))