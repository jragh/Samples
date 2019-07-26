#import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import csv
#import io
#import requests
from dash.dependencies import Input, Output, State
from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
import pyEX
import plotly.graph_objs as go
from datetime import date
from dateutil.relativedelta import relativedelta
from iexfinance.data_apis import get_data_points

token = 'pk_85bb1ef6118d470a8088cba709e9a103'
a = pd.read_csv(r'C:\Users\Jordan\Desktop\Github\stock_symbols.csv')

search_dict = [{'label': """{0}: {1}""".format(a.loc[i, 'symbol'], a.loc[i, 'name']), 'value': """{0}""".format(a.loc[i, 'symbol'])} for i in a.index]
stock_header_dict = {}
start = (date.today() - relativedelta(months=6))
end = date.today()

#### CSS Styling that we can change to have better white space etc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions=True

#### Layout which holds everything

app.layout = html.Div([html.H1('Stock Search'),
	dcc.Dropdown(id='stock-dropdown', placeholder = 'Pick Stocks From Here...', searchable = True, options = search_dict),
	html.Div(id='stock-search-results'),
	html.Br(),
	html.H4(id='header-1',style={'color': '#0189aa'}),
	html.H6(id='header-2'),
	html.H6(id='header-3'),
	html.H6(id='header-4'),
	html.H6(id='header-5'),
	html.H6(id='header-6'),
	html.H6(id='header-7'),
	dcc.Graph(id='candlestick-main')
	], style={'height':'100vh'})

@app.callback(Output('stock-search-results', 'children'),
	[Input('stock-dropdown', 'value')])
def generate_results(dd_input):
	if dd_input:
		name_extract = a.loc[a['symbol'] == dd_input, 'name'].iloc[0]
		return "You have chosen {0}: {1}".format(dd_input, name_extract)


@app.callback(
	[Output('header-1', 'children'),Output('header-2', 'children'), Output('header-3', 'children'), Output('header-4', 'children'), Output('header-5', 'children'), Output('header-6', 'children'), Output('header-7', 'children')],
	[Input('stock-dropdown', 'value')])
def generate_header(dd_input2):
	global q_display

	if dd_input2 is None:
		raise PreventUpdate
	sym = Stock(dd_input2,token=token)
	q_display = sym.get_quote()
	#stock_header_dict[dd_input2] = {k: v for k, v in q_display.items() if k in ['symbol', 'open', 'close', 'high', 'low', 'latestPrice', 'latestVolume', 'companyName']}
	return """{0} ({1})""".format(q_display['companyName'], q_display['symbol']), """Latest Price Sold: {0}""".format(get_data_points(q_display['symbol'], "QUOTE-LATESTPRICE")),"Open Price: {0}".format(get_data_points(q_display['symbol'], "QUOTE-OPEN")), """Close Price: {0}""".format(get_data_points(q_display['symbol'], "QUOTE-CLOSE")),"""High Price: {0}""".format(get_data_points(q_display['symbol'], "QUOTE-HIGH")), """Low Price: {0}""".format(get_data_points(q_display['symbol'], "QUOTE-LOW")), """Latest Volume Traded: {0}""".format(get_data_points(q_display['symbol'], "QUOTE-LATESTVOLUME"))


@app.callback(
	Output('candlestick-main', 'figure'),
	[Input('stock-dropdown','value')])
def generate_candlestick(dd_input3):
	if dd_input3 is None:
		raise PreventUpdate
	symbol_extract = a.loc[a['symbol'] == dd_input3, 'symbol'].iloc[0]

	hist_data = get_historical_data(symbol_extract, start, end, output_format='pandas', token = token)

	## Data Traces for Data Display Inside the Graph
	trace1 = go.Candlestick(x=hist_data.index, open = hist_data['open'], high= hist_data['high'], low= hist_data['low'], close=hist_data['close'], yaxis = 'y2', 
	increasing = dict(line=dict(color='#49BEB7')), decreasing = dict(line=dict(color='#FF5959')), name = 'Price Change')
	trace2 = go.Scatter(x=hist_data.index, y = hist_data.close.rolling(window=20).mean(), name='20 Day Simple Moving Average', mode='lines', yaxis = 'y2', 
	connectgaps=True, line=dict(color='#facf5a', width=0.75))
	trace3 = go.Scatter(x=hist_data.index, y = hist_data.close.ewm(span=20, adjust=False).mean(), name='20 Day Exponential Moving Average', mode='lines', yaxis = 'y2', 
	connectgaps=True, line=dict(color='#F71735', width=0.75))
	trace4 = go.Scatter(x=hist_data.index, y = (hist_data.close.rolling(window=20).mean() - (hist_data.close.rolling(window=20).std()*2.0)), name='Lower Bollinger Band (20 Days)', yaxis = 'y2', 
	mode='lines', connectgaps=True, line=dict(color='#293462', width=0.5))
	trace5 = go.Scatter(x=hist_data.index, y = (hist_data.close.rolling(window=20).mean() + (hist_data.close.rolling(window=20).std()*2.0)), name='Upper Bollinger Band (20 Days)', yaxis = 'y2', 
	mode='lines', connectgaps=True, line=dict(color='#293462', width=0.5))
	trace6 = go.Bar(x=hist_data.index, y=hist_data.volume, name='Volume Traded', marker = dict(color='#DCDCDC', line=dict(color='#808080', width=.75)), yaxis='y')

	## Layout Display for our Application
	layout =go.Layout(yaxis={'domain':[0,0.1],'showticklabels':False, 'title':'Volume Traded', 'side':'right'}, 
		yaxis2={'domain':[0.1, 0.8], 'showticklabels':True, 'title':'Price', 'side':'left', }, title='60 Day Overview: {0} ({1})'.format(q_display['companyName'], q_display['symbol']),
		xaxis=dict(rangeslider=dict(visible=False), type='date'))
	figure = {'data':[trace1, trace2, trace3, trace4, trace5, trace6], 'layout':layout}

	return figure
	
	#layout = {'title':'Test Plot', 'yaxis':dict(domain = [0, 0.2], showticklabels = False), 'yaxis2' : dict(domain = [0.2, 0.8])}


if __name__ == '__main__':
	app.run_server(debug=True, port=8055)
