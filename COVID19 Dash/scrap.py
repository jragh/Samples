import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from COVID19_Diff import calc_diff_country
from datetime import datetime

urls = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']

final_df = pd.read_csv('C:/Users/Jordan/Documents/COVID19/final_df.csv')



#print(final_df)
#print(final_df.Country_Region.unique())

mort = final_df.groupby(['Country_Region'])['Date'].max().reset_index()
mort = pd.merge(mort, final_df, on=['Country_Region', 'Date'], how='left')
mort['Mortality_Percent'] = (mort['Deaths'] / mort['Confirmed'])*100.00
print(mort.sort_values(by=['Confirmed'], ascending=False).head(20))

#.iloc[:, 0])

#print(final_df.loc[final_df['Continent'].notna(), 'Country_Region'].unique())

#print(final_df_state.loc[(final_df_state['Country_Region'] == 'Canada')])



# cases_1000_start = final_df.loc[(final_df['Confirmed'] >= 1000) & (final_df['Country_Region'] != 'Cruise Ship')].groupby(['Country_Region']).min()['Date']
# cases_1000_start = cases_1000_start.reset_index()
# cases_1000_start = cases_1000_start.rename(columns={"Date":"Start_Date"})
# final_df['Country_Region'] = final_df['Country_Region'].str.strip()
# cases_1000_start = pd.merge(cases_1000_start,final_df, on = ['Country_Region'],how='right')
# cases_1000_start['Start_Date'] = pd.to_datetime(cases_1000_start['Start_Date'])
# cases_1000_start['Date'] =  pd.to_datetime(cases_1000_start['Date'])
# cases_1000_start = cases_1000_start[cases_1000_start['Start_Date'].notna()]

# cases_1000_start['Days Since 1000 Cases'] = (cases_1000_start['Date'] - cases_1000_start['Start_Date']).dt.days


# fig1000 = []

# for group, dataframe in cases_1000_start.groupby(by='Country_Region'):
#     di = dataframe.sort_values(by=['Days Since 1000 Cases'])
#     trace = go.Scatter(x=di['Days Since 1000 Cases'].tolist(),
#     y=di['Confirmed'].tolist(),
#     mode='lines',
#     line=dict(color=colors_dict_global[list(di.loc[:, 'Continent'])[0]], width=0.5),
#     opacity=0.6,
#     text= str(group),
#     legendgroup=list(di.loc[:, 'Continent'])[0],
#     hovertemplate='<b>%{text}</b><br>'+'<br>Confirmed Cases: %{y}<br>'+'Days Since First 1000 Cases: %{x}<br>')

#     fig1000.append(trace)

# print(fig1000)


# colors_dict_global = {'Europe':'#1D6996','Asia':'#CC503E','Africa':'#94346E', 'North America':'#38A6A5', 'Middle East': '#EDAD08', 'South America':'#E17C05', 'Caribbean & Central America':'#0F8554', 'Oceania':'#73AF48'}

# deaths_100_start = final_df.loc[(final_df['Deaths'] >= 100) & (final_df['Country_Region'] != 'Cruise Ship')].groupby(['Country_Region']).min()['Date']
# deaths_100_start = deaths_100_start.reset_index()
# deaths_100_start = deaths_100_start.rename(columns={"Date":"Start_Date"})
# final_df['Country_Region'] = final_df['Country_Region'].str.strip()
# deaths_100_start = pd.merge(deaths_100_start,final_df, on = ['Country_Region'],how='right')
# deaths_100_start['Start_Date'] = pd.to_datetime(deaths_100_start['Start_Date'])
# deaths_100_start['Date'] =  pd.to_datetime(deaths_100_start['Date'])
# deaths_100_start = deaths_100_start[deaths_100_start['Start_Date'].notna()]
# deaths_100_start['Days Since 100 Deaths'] = (deaths_100_start['Date'] - deaths_100_start['Start_Date']).dt.days

# fig100 = []

# for group, dataframe in deaths_100_start.groupby(by='Country_Region'):
#     di = dataframe.sort_values(by=['Days Since 100 Deaths'])
#     trace = go.Scatter(x=di['Days Since 100 Deaths'].tolist(),
#     y=di['Deaths'].tolist(),
#     mode='lines',
#     line=dict(color=colors_dict_global[list(di.loc[:, 'Continent'])[0]], width=0.5),
#     opacity=0.6,
#     text= str(group),
#     legendgroup=list(di.loc[:, 'Continent'])[0],
#     hovertemplate='<b>%{text}</b><br>'+'<br>Confirmed Cases: %{y}<br>'+'Days Since First 1000 Cases: %{x}<br>')

#     fig100.append(trace)



# print(fig100)
