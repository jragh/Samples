import pandas as pd
#import io
#import requests
#from iexfinance.refdata import get_iex_symbols
#from iexfinance.stocks import Stock
#from iexfinance.stocks import get_historical_data
from datetime import datetime
import pyEX
#import csv
import sqlalchemy
from sqlalchemy import create_engine
import plotly.graph_objs as go
import plotly.offline as po

a = pyEX.bulkBatch(pyEX.symbolsList(), ['chart'], '6m')

hist_data = pd.DataFrame.from_dict(a['AAPL']['chart'])
print(hist_data.head())
print(hist_data.columns.values)
print(a['AAPL']['chart'])

trace1 = go.Candlestick(x=hist_data['date'], open = hist_data['open'], high= hist_data['high'], low= hist_data['low'], close=hist_data['close'], yaxis = 'y2', 
	increasing = dict(line=dict(color='#49BEB7')), decreasing = dict(line=dict(color='#FF5959')))
trace2 = go.Scatter(x=hist_data['date'], y = hist_data.close.rolling(window=20).mean(), name='20 Day SMA', mode='lines', yaxis = 'y2', 
	connectgaps=True, line=dict(color='#facf5a', width=0.75))
trace3 = go.Scatter(x=hist_data['date'], y = (hist_data.close.rolling(window=20).mean() - (hist_data.close.rolling(window=20).std()*2.0)), name='Lower Bollinger Band (20 Days)', yaxis = 'y2', 
	mode='lines', connectgaps=True, line=dict(color='#293462', width=0.5))
trace4 = go.Scatter(x=hist_data['date'], y = (hist_data.close.rolling(window=20).mean() + (hist_data.close.rolling(window=20).std()*2.0)), name='Upper Bollinger Band (20 Days)', yaxis = 'y2', 
	mode='lines', connectgaps=True, line=dict(color='#293462', width=0.5))
trace5 = go.Bar(x=hist_data.date, y=hist_data.volume, name='Volume Traded', marker = dict(color='#DCDCDC', line=dict(color='#808080', width=.75)), yaxis='y')

po.plot({'data': [trace1, trace2, trace3, trace4, trace5], 'layout': {'title':'Test Plot', 'yaxis':dict(domain = [0, 0.2], showticklabels = False), 'yaxis2' : dict(domain = [0.2, 0.8])}}, auto_open=True, image='png', image_filename='plot_image',
	output_type='file', image_width=800, image_height=600, 
	filename='temp-plot.html', validate=False)
