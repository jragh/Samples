import pandas as pd
import io
import requests
from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock
from datetime import date
from dateutil.relativedelta import relativedelta
from iexfinance.stocks import get_historical_data
from iexfinance.data_apis import get_data_points

#### Method call to return all of the current symbols into 
#a = get_symbols(output_format='pandas', token='pk_85bb1ef6118d470a8088cba709e9a103')

#### Writing the Pandas Dataframe to a CSV to call symbols locally from the main app
#a.to_csv(path_or_buf=r'C:\Users\Jordan\Desktop\Github\stock_symbols.csv',index=False)
