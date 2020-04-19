import pandas as pd
import numpy as np

final_df = pd.read_csv('C:/Users/Jordan/Documents/COVID19/final_df.csv')

#print(final_df.loc[final_df['Country_Region'] == 'Canada'])

def calc_diff_country(df, group_col='Country_Region', date_col='Date'):
	blank_df = pd.DataFrame(columns=['Country_Region', 'Date', 'Confirmed', 'Deaths', 'Recovered'])

	for i in list(df[group_col].unique()):
		temp = df.loc[(df[group_col] == i)].sort_values([group_col, date_col])
		temp['Confirmed_Diff'] = temp['Confirmed'].diff()
		temp['Deaths_Diff'] = temp['Deaths'].diff()
		temp['Recovered_Diff'] = temp['Recovered'].diff()

		temp = temp.fillna(0)
		temp[date_col] = pd.to_datetime(temp[date_col]) 

		blank_df = blank_df.append(temp, ignore_index=True, sort = False)

	return blank_df




#final_df = calc_diff_country(final_df)

#final_df = final_df.loc[final_df['Country_Region'] == 'Canada']

#print()

#print(final_df.loc[final_df['Country_Region'] == 'Canada'])
#print(final_df.info())
