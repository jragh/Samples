import pandas as pd
import io
import requests

api_key = 'FHU37C3WLEO737CY'


url = 'https://www.alphavantage.co/query?function=SECTOR&apikey={0}'.format(api_key)
s = requests.get(url).content

s = pd.read_json(io.StringIO(s.decode('utf-8')))
print(s.columns.values)
print(s.iloc[:, 1])
