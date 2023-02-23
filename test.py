import hmac
import hashlib
import json

secret = "WqCBpR6JfSSkzciYGslKC3fjcjlDrvjsLLWc"

def get_signature(param_str):
    return str(hmac.new(bytes(secret, "utf-8"), bytes(param_str, "utf-8"), digestmod="SHA256").hexdigest())

url = "https://api-testnet.bybit.com"

api_key = "Y30aFoxzTGQaCTybPC"
leverage = 1
order_type = "Limit"#market
price = 25000
qty = 1
side = "Buy"
stop_loss = 22000
symbol = "BTCUSDT"
take_profit = 26000
time_in_force = "GoodTillCancel"

def place_active_order(symbol, side, qty, price, stop_loss, take_profit, order_type="Limit",time_in_force='GoodTillCancel'):
    timestamp = int(time.time() * 1000)
    param_str = f"api_key={api_key}&leverage={leverage}&order_type={order_type}&price={price}&qty={qty}&side={side}&stop_loss={stop_loss}&symbol={symbol}&take_profit={take_profit}&time_in_force={time_in_force}&timestamp={timestamp}"
    sign = get_signature(param_str)
    data = {
        "api_key": api_key,
        "leverage": leverage,
        "timestamp": timestamp,

        "side": side,
        "symbol": symbol,
        "order_type": order_type,
        "qty": qty,
        "price": price,
        "time_in_force": time_in_force,
        "take_profit": take_profit,
        "stop_loss": stop_loss,
        "sign": sign
    }
    r = requests.post(url + "/contract/v3/private/order/create", data)
    print(r.text)

place_active_order(symbol, side, qty, price, stop_loss, take_profit, order_type, time_in_force)