import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.exceptions import PreventUpdate
import csv
import io
import requests
from dash.dependencies import Input, Output, State
from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock

token = ''
#a = get_symbols(output_format='pandas', token=token)
a = pd.read_csv(r'C:\Users\Jordan\Desktop\Github\stock_symbols.csv')

search_dict = [{'label': """{0}: {1}""".format(a.loc[i, 'symbol'], a.loc[i, 'name']), 'value': """{0}""".format(a.loc[i, 'symbol'])} for i in a.index]
stock_header_dict = {}

#### CSS Stylign that we can change to have better white space etc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions=True

#### Layout which hlds everything

app.layout = html.Div([html.H1('Stock Search'),
	dcc.Dropdown(id='stock-dropdown', placeholder = 'Pick Stocks From Here...', searchable = True, options = search_dict),
	html.Div(id='stock-search-results'),
	html.Br(),
	html.H2(id='header-1',style={'color': '#0189aa'}),
	html.H5(id='header-2'),
	html.H5(id='header-3'),
	html.H5(id='header-4'),
	html.H5(id='header-5'),
	html.H5(id='header-6'),
	html.H5(id='header-7')
	])

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
	if dd_input2 is None:
		raise PreventUpdate
	sym = Stock(dd_input2,token=token)
	q_display = sym.get_quote()
	#stock_header_dict[dd_input2] = {k: v for k, v in q_display.items() if k in ['symbol', 'open', 'close', 'high', 'low', 'latestPrice', 'latestVolume', 'companyName']}
	return """{0} ({1})""".format(q_display['companyName'], q_display['symbol']), """Latest Price Sold: {0}""".format(q_display['latestPrice']), """Open Price: {0}""".format(q_display['open']), """Close Price: {0}""".format(q_display['close']),"""High Price: {0}""".format(q_display['high']), """Low Price: {0}""".format(q_display['low']), """Latest Volume Traded: {0}""".format(q_display['latestVolume'])


if __name__ == '__main__':
	app.run_server(debug=True, port=8055)
