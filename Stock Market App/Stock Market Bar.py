import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import csv
import io
import requests
from dash.dependencies import Input, Output, State
from iexfinance.refdata import get_symbols

token = ''
a = get_symbols(output_format='pandas', token=token)
search_dict = [{'label': """{0}: {1}""".format(a.loc[i, 'symbol'], a.loc[i, 'name']), 'value': """{0}""".format(a.loc[i, 'symbol'])} for i in a.index]

#### CSS Stylign that we can change to have better white space etc
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.supress_callback_exceptions=True

#### Layout which hlds everything

app.layout = html.Div([html.H1('Stock Search'),
	dcc.Dropdown(id='stock-dropdown', placeholder = 'Pick Stocks From Here...', searchable = True, options = search_dict),
	html.Div(id='stock-search-results')
	])

@app.callback(Output('stock-search-results', 'children'),
	[Input('stock-dropdown', 'value')])
def generate_results(dd_input):
	if dd_input:
		name_extract = a.loc[a['symbol'] == dd_input, 'name'].iloc[0]
		return "You have chosen {0}: {1}".format(dd_input, name_extract)

if __name__ == '__main__':
    app.run_server(debug=True, port=8052)
