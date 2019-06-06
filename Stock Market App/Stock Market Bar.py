import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import io
import requests
from dash.dependencies import Input, Output, State

#### CSS Stylign that we can change to have better white space etc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

api_key = 'FHU37C3WLEO737CY'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions=True

#### Layout which hlds everything
#### 



app.layout = html.Div([html.H1('Stock Search'),
	dcc.Input(id='stock-search', value='Search your Stock Here', type='text'),
	html.Div(id = 'stock-dropdown'),
	#dcc.Dropdown(id='stock-dropdown', placeholder = 'Pick Stocks from Here', searchable = True, options = []),
	html.Div(id='stock-search-results')
	])

#@app.callback(Output('stock-dropdown', 'value'),
#	[Input('stock-search', 'value')])
#def reset_sd(ss_inp):
#	return ''

@app.callback(Output('stock-dropdown', 'children'),
[Input('stock-search', 'value')])
def generate_search_stock(search_val):
	if search_val:
		url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={0}&apikey={1}&datatype=csv'.format(search_val, api_key)
		s = requests.get(url).content
		s1 = pd.read_csv(io.StringIO(s.decode('utf-8')))
		search_dict = [{'label': """{0}: {1}""".format(s1.loc[i, 'symbol'], s1.loc[i, 'name']), 'value': """{0}""".format(s1.loc[i, 'symbol'], s1.loc[i, 'name'])} for i in s1.index]
		return dcc.Dropdown(id ='dropdown-true',placeholder = 'Pick Stocks From Here...', searchable=False, options = search_dict)

@app.callback(Output('stock-search-results', 'children'),
	[Input('dropdown-true', 'value')])
def generate_results(dd_input):
	if dd_input:
			return "You have chosen {0}".format(dd_input)




if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
