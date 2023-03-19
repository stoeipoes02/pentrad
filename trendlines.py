import plotly.graph_objects as go
import pandas as pd
from matplotlib import pyplot
import numpy as np

# reading in the data
df = pd.read_csv("EURUSD_Candlestick_4_Hour_ASK_05.05.2003-16.10.2021.csv")
df.columns=['time', 'open', 'high', 'low', 'close', 'volume']
#Check if NA values are in data
df=df[df['volume']!=0]
df.reset_index(drop=True, inplace=True)
df.isna().sum()

print(df.head(6))

backcandles = 60
window = 10
candleid = 1


maxim = np.array([])
minim = np.array([])
xxmin = np.array([])
xxmax = np.array([])

for i in range(200, 2000, 200):

    # minimums
    minim = np.append(minim, df.low.iloc[i:i+window].min())
    xxmin = np.append(xxmin, df.low.iloc[i:i+window].idxmin())

    # maximums
    maxim = np.append(maxim, df.high.iloc[i:i+window].max())
    xxmax = np.append(xxmax, df.high.iloc[i:i+window].idxmax())

slmin, intercmin = np.polyfit(xxmin, minim,1)
slmax, intercmax = np.polyfit(xxmax, maxim,1)

dfpl = df[1:2200]  
fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                open=dfpl['open'],
                high=dfpl['high'],
                low=dfpl['low'],
                close=dfpl['close'])])

fig.add_trace(go.Scatter(x=xxmin, y=slmin*xxmin + intercmin, mode='lines', name='min slope'))
fig.add_trace(go.Scatter(x=xxmax, y=slmax*xxmax + intercmax, mode='lines', name='max slope'))


fig.show()


# import numpy as np
# from matplotlib import pyplot
# backcandles= 100
# brange = 50 #should be less than backcandles
# wind = 5

# candleid = 10100

# optbackcandles= backcandles
# sldiff = 100
# sldist = 10000
# for r1 in range(backcandles-brange, backcandles+brange):
#     maxim = np.array([])
#     minim = np.array([])
#     xxmin = np.array([])
#     xxmax = np.array([])
    
#     for i in range(candleid-r1, candleid+1, wind):
#         minim = np.append(minim, df.low.iloc[i:i+wind].min())
#         xxmin = np.append(xxmin, df.low.iloc[i:i+wind].idxmin())
#     for i in range(candleid-r1, candleid+1, wind):
#         maxim = np.append(maxim, df.high.loc[i:i+wind].max())
#         xxmax = np.append(xxmax, df.high.iloc[i:i+wind].idxmax())
#     slmin, intercmin = np.polyfit(xxmin, minim,1)
#     slmax, intercmax = np.polyfit(xxmax, maxim,1)
    
#     dist = (slmax*candleid + intercmax)-(slmin*candleid + intercmin)
#     if(dist<sldist): #abs(slmin-slmax)<sldiff and
#         #sldiff = abs(slmin-slmax)
#         sldist = dist
#         optbackcandles=r1
#         slminopt = slmin
#         slmaxopt = slmax
#         intercminopt = intercmin
#         intercmaxopt = intercmax
#         maximopt = maxim.copy()
#         minimopt = minim.copy()
#         xxminopt = xxmin.copy()
#         xxmaxopt = xxmax.copy()

        
# print(optbackcandles)
# dfpl = df[candleid-wind-optbackcandles-backcandles:candleid+optbackcandles]  
# fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
#                 open=dfpl['open'],
#                 high=dfpl['high'],
#                 low=dfpl['low'],
#                 close=dfpl['close'])])

# adjintercmax = (df.high.iloc[xxmaxopt] - slmaxopt*xxmaxopt).max()
# adjintercmin = (df.low.iloc[xxminopt] - slminopt*xxminopt).min()
# fig.add_trace(go.Scatter(x=xxminopt, y=slminopt*xxminopt + adjintercmin, mode='lines', name='min slope'))
# fig.add_trace(go.Scatter(x=xxmaxopt, y=slmaxopt*xxmaxopt + adjintercmax, mode='lines', name='max slope'))
# fig.show()