import os, csv
import talib
import yfinance as yf
from flask import Flask, escape, requests, render_template
from patterns import candlestick_pattern

data = yf.download("SPY", start="2022-05-26", end="2023-01-26")

engulfing = talib._ta_lib.CDLDOJI(data['Open'], data['High'], data['Low'], data['Close'])
print(engulfing[engulfing != 0])
data['engulfing'] = engulfing
print(data[data['engulfing'] !=0])
#print(talib.get_functions())
