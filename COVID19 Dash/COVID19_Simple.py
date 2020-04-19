# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 00:27:31 2020

@author: Jordan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def gdata_creation(url1, url2, url3):
    raw_confirmed = pd.read_csv(url1)
    raw_deaths = pd.read_csv(url2)
    raw_recovered = pd.read_csv(url3)
    
    raw_confirmed = raw_confirmed.drop(['Province/State', 'Lat', 'Long'],
                                       axis = 1)
    raw_deaths = raw_deaths.drop(['Province/State', 'Lat', 'Long'],
                                 axis = 1)
    raw_recovered = raw_recovered.drop(['Province/State', 'Lat', 'Long'],
                                       axis = 1)
    
    cols_rc = list(raw_confirmed.columns.values)
    del cols_rc[0]
    
    ccc = raw_confirmed.groupby(['Country/Region']).sum().reset_index()
    ddd = raw_deaths.groupby(['Country/Region']).sum().reset_index()
    rrr = raw_recovered.groupby(['Country/Region']).sum().reset_index()
    
    
    ### Confirmed Dictionary ###
    c_dict = {}

    for i in list(ccc['Country/Region'].unique()):
        c_dict[i] = {j: ccc.loc[(ccc['Country/Region'] == i), j].values[0] for j in list(ccc.columns.values)[1:]}
        # for j in list(ccc.columns.values)[1:]:
        #     c_dict[i][j] = ccc.loc[(ccc['Country/Region'] == i), j].values[0]

    ### Deaths Dictionary ###
    d_dict = {}

    for i in list(ddd['Country/Region'].unique()):
        d_dict[i] = {j: ddd.loc[(ddd['Country/Region'] == i), j].values[0] for j in list(ddd.columns.values)[1:]}
        # for j in list(ddd.columns.values)[1:]:
        #     d_dict[i][j] = ddd.loc[(ddd['Country/Region'] == i), j].values[0]

    ### Recovered Dictionary ###
    r_dict = {}

    for i in list(rrr['Country/Region'].unique()):
        r_dict[i] = {j: rrr.loc[(rrr['Country/Region'] == i), j].values[0] for j in list(rrr.columns.values)[1:]}
        # for j in list(rrr.columns.values)[1:]:
        #     r_dict[i][j] = rrr.loc[(rrr['Country/Region'] == i), j].values[0]
            
    
    final_df = pd.DataFrame(columns = ['Country_Region', 'Date', 'Confirmed', 'Deaths', 'Recovered'])


    for i in c_dict.keys():
        for j, k in c_dict[i].items():
            final_df = final_df.append({'Country_Region': i, 'Date': j, 'Confirmed': k}, ignore_index=True)
        for l, m in d_dict[i].items():
            final_df.loc[(final_df['Country_Region'] == i) & (final_df['Date'] == l), 'Deaths'] = m
        for n, o in r_dict[i].items():
            final_df.loc[(final_df['Country_Region'] == i) & (final_df['Date'] == n), 'Recovered'] = o
    
    return final_df
    

urls = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']

final_df = gdata_creation(urls[0], urls[1], urls[2])

continents = pd.read_csv('C:/Users/Jordan/Documents/COVID19/final_df_continents.csv')

final_df = pd.merge(final_df, continents, on='Country_Region', how='left')

final_df = final_df.loc[final_df['Continent'].notna()]

final_df['Date'] = pd.to_datetime(final_df['Date'])

country_pops = pd.read_csv('C:\\Users\\Jordan\\Documents\\COVID19\\Country_Populations.csv')

final_df = pd.merge(final_df, country_pops, on='Country_Region', how='left')

final_df['Date'] = pd.to_datetime(final_df['Date'])

final_df.to_csv('C:/Users/Jordan/Documents/COVID19/final_df.csv')

#print(final_df.loc[final_df['Country_Region'] == 'Canada'])