# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 01:03:35 2020

@author: Jordan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
## from COVID19_Simple import *
from COVID19_Diff import calc_diff_country
### Dash Stuff ###
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import math

### Initial Code Block; Set Up Data ###
urls = ['https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']


### Base Country Data (and Transformations)
final_df = pd.read_csv('C:/Users/Jordan/Documents/COVID19/final_df.csv')
final_df = calc_diff_country(final_df)
final_df['Date'] = pd.to_datetime(final_df['Date'])

final_df['Country_Region'] = final_df['Country_Region'].astype(str)


### 1000 Cases, 10 Deaths, 10 Recovered ### (Global)
## 1000 Cases ##
cases_1000_start = final_df.loc[(final_df['Confirmed'] >= 1000) & (final_df['Country_Region'] != 'Cruise Ship')].groupby(['Country_Region']).min()['Date']
cases_1000_start = cases_1000_start.reset_index()
cases_1000_start = cases_1000_start.rename(columns={"Date":"Start_Date"})
final_df['Country_Region'] = final_df['Country_Region'].str.strip()
cases_1000_start = pd.merge(cases_1000_start,final_df, on = ['Country_Region'],how='right')
cases_1000_start['Start_Date'] = pd.to_datetime(cases_1000_start['Start_Date'])
cases_1000_start['Date'] =  pd.to_datetime(cases_1000_start['Date'])
cases_1000_start = cases_1000_start[cases_1000_start['Start_Date'].notna()]
cases_1000_start['Days Since 1000 Cases'] = (cases_1000_start['Date'] - cases_1000_start['Start_Date']).dt.days


## 100 Deaths ##
deaths_100_start = final_df.loc[(final_df['Deaths'] >= 100) & (final_df['Country_Region'] != 'Cruise Ship')].groupby(['Country_Region']).min()['Date']
deaths_100_start = deaths_100_start.reset_index()
deaths_100_start = deaths_100_start.rename(columns={"Date":"Start_Date"})
final_df['Country_Region'] = final_df['Country_Region'].str.strip()
deaths_100_start = pd.merge(deaths_100_start,final_df, on = ['Country_Region'],how='right')
deaths_100_start['Start_Date'] = pd.to_datetime(deaths_100_start['Start_Date'])
deaths_100_start['Date'] =  pd.to_datetime(deaths_100_start['Date'])
deaths_100_start = deaths_100_start[deaths_100_start['Start_Date'].notna()]
deaths_100_start['Days Since 100 Deaths'] = (deaths_100_start['Date'] - deaths_100_start['Start_Date']).dt.days

## Mortality Ratios ##
mort = final_df.groupby(['Country_Region'])['Date'].max().reset_index()
mort = pd.merge(mort, final_df, on=['Country_Region', 'Date'], how='left')
mort['Mortality_Percent'] = (mort['Deaths'] / mort['Confirmed'])*100.00


colors_dict_global = {'Europe':'#1D6996','Asia':'#CC503E','Africa':'#94346E', 'North America':'#38A6A5', 'Middle East': '#EDAD08', 'South America':'#E17C05', 'Caribbean & Central America':'#0F8554', 'Oceania':'#73AF48'}

### Dash Portion of the Script ###
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

app.layout = html.Div(children=[
    html.H2(children='COVID-19 Dashboard'),
    html.H4(children='A Basic Dashboard to Help Track the COVID-19 Pandemic'),
    html.Br(),
    html.H5(children='Global View'),
    html.P(children='The Global View highlights how Covid-19 is affecting countries across the world, and how the pandemic is expanding on a country by country basis. The Global View includes the following:'),
    html.Div([html.Ul([html.Li([html.B('Cumulative Cases by Country Since First 1000 Cases: '),'This allows us to see how cases are spreading since the first 1000 Cases on a country by country basis']),
        html.Li([html.B('Cumulative Cases by Country Since First 100 Deaths: '),'This allows us to see COVID-19 fatalities since the first 100 Deaths on a country by country basis']),
        html.Li([html.B('Observed Case - Mortality Ratio (Top 20 Countries by Confirmed Cases): '), 'This allows us to see the percentage of COVID19 fatalities based on reported cases and deaths. (Note that reporting standards vary from country to country, so this is for illustrative purposes only)']),
        html.Li([html.B('Recoveries vs. Deaths By Country (Countries with over 100 deaths and 100 recoveries: '), 'This plots Recoveries against Deaths on a country by country basis. (Note that reporting standards vary from country to country, so this is for illustrative purposes only)'])])], style={'font-size': 12}),
    html.Br(),
    dcc.Dropdown(id='global-dropdown', options=[{'label':y, 'value':y} for y in ['Global Cases Trend', 'Global Deaths Trend', '% Mortality by Confirmed Cases (Top 20 Countries)','Recoveries vs. Deaths By Country']], placeholder = 'Pick Graphs From Here...'),
    dcc.Graph(id='global-box-1'),
    html.Br(),
    html.H5(children='Country View'),
    html.P('The Country view allows us to see a closer look on how the COVID-19 Pandemic has expanded. As opposed to a high level aggregation, the Country View provides a day by day time series analysis of the effects of COVID-19. The Country View includes the following:'),
    html.Div(style={'font-size': 12}, children=[html.Ul([html.Li([html.B('Confirmed: '), 'Cumulative Confirmed Cases of COVID-19 since January 22nd, 2020']),
        html.Li([html.B('Recovered: '), 'Cumulative Recovered Cases of COVID-19 since January 22nd, 2020']),
        html.Li([html.B('Deaths: '),'Cumulative Deaths from COVID-19 since January 22nd, 2020']),
        html.Li([html.B('Total and Daily Confirmed Cases: '), 'Cumulative and Daily Cases Since January 22nd, 2020. This illustrates the curve of daily cases in relation to the total cases for a country'])])]),
    dcc.Dropdown(id='main-dropdown', options=[{'label': x, 'value': x} for x in list(final_df.Country_Region.unique())], placeholder = 'Pick a Country From Here...'),
    dcc.Dropdown(id='main-dropdown-2', placeholder = 'Pick Graphs From Here...'),
    dcc.Graph(id='box-1'),
    html.Div([html.Div([html.H6(children='Most Recent New Cases'), html.H1(id='btext1'), dcc.Graph(id='subplot1')], className = 'four columns', style={'color': '#648FFF'}),
     html.Div([html.H6(children='Most Recent Daily Deaths'), html.H1(id='btext2'), dcc.Graph(id='subplot2')], className = 'four columns',  style={'color': '#DC267F'}),
       html.Div([html.H6(children='Most Recent Daily Recovered'), html.H1(id='btext3'), dcc.Graph(id='subplot3')], className = 'four columns', style={'color': '#009E73', 'layout':'right'})], className="row")
])

## Callback Functionality ## 
@app.callback(
    Output(component_id='global-box-1', component_property='figure'),
    [Input(component_id='global-dropdown', component_property='value')])

def global_update(select_global):
    if select_global == 'Global Cases Trend' or select_global is None:

        fig1000 = []
        anno = []

        for group, dataframe in cases_1000_start.groupby(by='Country_Region'):
            di = dataframe.sort_values(by=['Days Since 1000 Cases'])
            trace = go.Scatter(x=di['Days Since 1000 Cases'].tolist(),
            y=di['Confirmed'].tolist(),
            mode='lines',
            line=dict(color=colors_dict_global[list(di.loc[:, 'Continent'])[0]], width=1),
            opacity=0.6,
            text= di.Country_Region.tolist(),
            legendgroup=list(di.loc[:, 'Continent'])[0],
            hovertemplate='<b>%{text}</b><br>'+'<br>Confirmed Cases: %{y}<br>'+'Days Since First 1000 Cases: %{x}<br>',
            showlegend=False)

            a = {'x': int(di['Days Since 1000 Cases'].max()+1.5),
            'y':np.log10(int(di['Confirmed'].max())),
            'xref':'x', 'yref':'y',
            'showarrow':False,
            'text':list(di.loc[:, 'Country_Region'])[0],
            'xanchor':'right', 
            'yanchor':'middle',
            'align':'center',
            'font':{'size':8, 'color':'black'},
            'bordercolor':"#ffffff",
            'borderwidth':1,
            'borderpad':1,
            'bgcolor':"#ffffff",
            'opacity':0.6}

            fig1000.append(trace)
            anno.append(a)

        fig1000.append(go.Scatter(x=list(np.arange(cases_1000_start['Days Since 1000 Cases'].max())),
            y = [1000 * (math.exp(0.2310491 * i)) for i in list(np.arange(cases_1000_start['Days Since 1000 Cases'].max()))],
            name='Cases Double Every 3 Days',
            mode='lines',
            opacity=.25,
            line = dict(color='grey', width=3, dash='dash'),
            text=['# of Cases Double Every 3 Days'],
            hovertemplate='<b>Cases Double Every 3 Days</b>',
            showlegend=True))

        fig1000.append(go.Scatter(x=list(np.arange(cases_1000_start['Days Since 1000 Cases'].max())),
            y = [1000 * (math.exp(0.099021 * i)) for i in list(np.arange(cases_1000_start['Days Since 1000 Cases'].max()))],
            name='Cases Double Every 7 Days',
            mode='lines',
            opacity=.25,
            line = dict(color='grey', width=3, dash='dot'),
            text=['# of Cases Double Every 7 Days'],
            hovertemplate='<b>Cases Double Every 7 Days</b>',
            showlegend=True))

        layout_global = go.Layout(yaxis={'title':'Number of Confirmed Cases', 'range':[np.log10(1000), np.log10(cases_1000_start['Confirmed'].max() * 1.10)], 'type':'log', 'fixedrange':True, 'linewidth':2, 'linecolor':'black', 'showgrid': False, 'dtick': 1, 'showline':True, 'mirror':False},
            title='Overall Confirmed Cases',
            xaxis={'title': 'Days Since First 1000 Cases', 'range': [0, cases_1000_start['Days Since 1000 Cases'].max()], 'fixedrange':True, 'linewidth':2, 'linecolor':'black', 'showgrid': False, 'showline':True, 'mirror':False}, height=750, hovermode='closest', annotations=anno)

        fig_global={'data':fig1000, 'layout': layout_global}
        return fig_global

    elif select_global == 'Global Deaths Trend':
        fig100 = []
        anno = []

        for group, dataframe in deaths_100_start.groupby(by='Country_Region'):
            di = dataframe.sort_values(by=['Days Since 100 Deaths'])
            trace = go.Scatter(x=di['Days Since 100 Deaths'].tolist(),
            y=di['Deaths'].tolist(),
            mode='lines',
            line=dict(color=colors_dict_global[list(di.loc[:, 'Continent'])[0]], width=1),
            opacity=0.6,
            text= di.Country_Region.tolist(),
            legendgroup=list(di.loc[:, 'Continent'])[0],
            hovertemplate='<b>%{text}</b><br>'+'<br>Deaths: %{y}<br>'+'Days Since First 1000 Cases: %{x}<br>',
            showlegend=False)

            a={'x': int(di['Days Since 100 Deaths'].max()+1.5),
            'y':np.log10(int(di['Deaths'].max())),
            'xref':'x', 'yref':'y',
            'showarrow':False,
            'text':list(di.loc[:, 'Country_Region'])[0],
            'xanchor':'right', 
            'yanchor':'middle',
            'align':'center',
            'font':{'size':8, 'color':'black'},
            'bordercolor':"#ffffff",
            'borderwidth':1,
            'borderpad':1,
            'bgcolor':"#ffffff",
            'opacity':0.6}

            fig100.append(trace)
            anno.append(a)

        fig100.append(go.Scatter(x=list(np.arange(deaths_100_start['Days Since 100 Deaths'].max())),
            y = [100 * (math.exp(0.2310491 * i)) for i in list(np.arange(deaths_100_start['Days Since 100 Deaths'].max()))],
            name='Deaths Double Every 3 Days',
            mode='lines',
            opacity=.25,
            line = dict(color='grey', width=3, dash='dash'),
            text=['# of Deaths Double Every 3 Days'],
            hovertemplate='<b>Deaths Double Every 3 Days</b>',
            showlegend=True))

        fig100.append(go.Scatter(x=list(np.arange(deaths_100_start['Days Since 100 Deaths'].max())),
            y = [100 * (math.exp(0.099021 * i)) for i in list(np.arange(deaths_100_start['Days Since 100 Deaths'].max()))],
            name='Deaths Double Every 7 Days',
            mode='lines',
            opacity=.25,
            line = dict(color='grey', width=3, dash='dot'),
            text=['# of Deaths Double Every 7 Days'],
            hovertemplate='<b>Deaths Double Every 7 Days</b>',
            showlegend=True))

        layout_global = go.Layout(yaxis={'title':'Number of Deaths', 'range':[np.log10(100), np.log10(cases_1000_start['Deaths'].max() * 1.10)], 'type':'log', 'fixedrange':True, 'linewidth':2, 'linecolor':'black', 'showgrid': False, 'dtick': 1, 'showline':True, 'mirror':False},
            title='Overall Deaths',
            xaxis={'title': 'Days Since First 100 deaths', 'range': [0, deaths_100_start['Days Since 100 Deaths'].max()], 'fixedrange':True, 'linewidth':2, 'linecolor':'black', 'showgrid': False, 'showline':True, 'mirror':False}, height=750, hovermode='closest', annotations=anno)

        fig_global={'data':fig100, 'layout': layout_global}
        return fig_global


    elif select_global == '% Mortality by Confirmed Cases (Top 20 Countries)':
        figmort = []
        anno =[]

        m = mort.sort_values(by=['Confirmed'], ascending=False).head(20)
        m = m.sort_values(by=['Mortality_Percent'], ascending=True).reset_index()

        for i in range(len(m)):

            m1 = m.loc[i, 'Country_Region']
            #m1 = [str(i) for i in m1]
            m2 = m.loc[i, 'Mortality_Percent']
            #m2 = [str(round(i, 2)) for i in m2]
            trace = go.Bar(name='Observed Case - Mortality Ratio',
            x = [m2],
            y= [m1],
            text = [round(m.loc[i, 'Mortality_Percent'], 2)],
            orientation ='h',
            textposition='auto',
            marker = dict(color='#FFB000', opacity=0.6, line=dict(color='rgba(255,176,0, 1)', width=1)),
            hovertemplate='<b>%{y}</b><br>'+'<br>Observed Case Mortaility Pct: %{text}&#37;<br>',
            showlegend=False)

            figmort.append(trace)

        layout_global = go.Layout(yaxis={'title':'Country / Region','fixedrange':True, 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Observed Case - Mortality Ratio',
            xaxis={'title': '% Mortality by Confirmed Cases (Top 20 Countries)', 'range': [0, m['Mortality_Percent'].max() + 2], 'fixedrange':True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=750, hovermode='closest')
        fig_global={'data':figmort, 'layout': layout_global}
        return fig_global


    elif select_global == 'Recoveries vs. Deaths By Country':
        figscat = []
        rc = mort.loc[(mort['Deaths'] >= 100) & (mort['Recovered'] >=100)].reset_index()

        for i in range(len(rc)):
            scat = go.Scatter(
                x=[rc.loc[i, 'Deaths']],
                y=[rc.loc[i, 'Recovered']],
                mode='markers+text',
                text=[rc.loc[i, 'Country_Region']],
                marker_color=(colors_dict_global[rc.loc[i, 'Continent']]),
                showlegend=False,
                marker=dict(size=12,line_width=1, opacity=0.75),
                hovertemplate='<b>%{text}</b><br>'+'<br>Recoveries: %{y}<br>'+'Deaths: %{x}<br>',
                textposition='bottom center',
                textfont=dict(size=10, color='rgba(0, 0, 0, 0.6)')
                )

            figscat.append(scat)

        figscat.append(go.Scatter(x=list(np.linspace(100, rc['Deaths'].max(), 3)),
            y = [i for i in list(np.linspace(100, rc['Deaths'].max(), 3))],
            mode='lines',
            name='Deaths = Recoveries',
            opacity=.25,
            line = dict(color='grey', width=1),
            text=['# of Deaths = # of Recoveries'],
            hovertemplate='<b># of Deaths = # of Recoveries</b>',
            showlegend=True))

        figscat.append(go.Scatter(x=list(np.linspace(100, rc['Deaths'].max(), 3)),
            y = [i*2 for i in list(np.linspace(100, rc['Deaths'].max(), 3))],
            mode='lines',
            name='2 Recoveries for Every Death',
            opacity=.25,
            line = dict(color='green', width=3, dash='dash'),
            text=['2 Recoveries for Every Death'],
            hovertemplate='<b>2 Recoveries for Every Death</b>',
            showlegend=True))

        figscat.append(go.Scatter(x=list(np.linspace(100, rc['Deaths'].max(), 3)),
            y = [i/2 for i in list(np.linspace(100, rc['Deaths'].max(), 3))],
            mode='lines',
            name='2 Deaths for Every Recovery',
            opacity=.25,
            line = dict(color='firebrick', width=3, dash='dash'),
            text=['2 Deaths for Every Recovery'],
            hovertemplate='<b>2 Deaths for Every Recovery</b>',
            showlegend=True))

        layout_global = go.Layout(yaxis={'title':'Number of Recoveries','fixedrange':True, 'automargin': True, 'range':[np.log10(100), np.log10(rc['Recovered'].max() * 1.10)], 'type':'log', 'linewidth':2, 'linecolor':'black', 'showgrid': False, 'dtick': 1, 'showline':True, 'mirror':False},
            title='Recoveries vs. Deaths, By Country',
            xaxis={'title': 'Number of Deaths','fixedrange':True, 'range':[np.log10(100), np.log10(rc['Deaths'].max() * 1.10)], 'type':'log', 'linewidth':2, 'linecolor':'black', 'showgrid': False, 'dtick': 1, 'showline':True, 'mirror':False}, height=750, hovermode='closest')

        fig_global={'data':figscat, 'layout': layout_global}
        return fig_global


@app.callback(
    [Output(component_id='main-dropdown-2', component_property = 'options'),
    Output(component_id='btext1', component_property='children'),
    Output(component_id='subplot1', component_property = 'figure'),
    Output(component_id='btext2', component_property='children'),
    Output(component_id='subplot2', component_property = 'figure'),
    Output(component_id='btext3', component_property='children'),
    Output(component_id='subplot3', component_property = 'figure')],
    [Input(component_id='main-dropdown', component_property = 'value')])

def update_country(selected_country):

    if selected_country is None:
        selected_country = 'Canada'

        options = ['Confirmed','Recovered','Deaths', 'Total and Daily Confirmed Cases']

        vals = [{'label': i, 'value': i} for i in options]

        trace_1 = [go.Bar(name='Daily Cases', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Confirmed_Diff'].tail(45), marker_color='#648FFF', opacity=0.6),
        go.Scatter(name='5 Day Moving Average', x = final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Confirmed_Diff'].tail(45).rolling(window=5).mean(), mode='lines', line=dict(color='#648FFF', width = 3))]
        layout_t1 = go.Layout(yaxis={'title': 'Number of Confirmed Cases', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Daily Confirmed Cases: {0} (Last 45 Days)'.format(selected_country),
            xaxis={'type': 'date', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=300, legend=dict(x=.2, y=-.15, orientation='h'))

        trace_2 = [go.Bar(name='Daily Deaths', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Deaths_Diff'].tail(45), marker_color='#DC267F', opacity=0.6),
        go.Scatter(name='5 Day Moving Average', x = final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Deaths_Diff'].tail(45).rolling(window=5).mean(), mode='lines', line=dict(color='#DC267F', width = 3))]
        layout_t2 = go.Layout(yaxis={'title': 'Number of Deaths', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Daily Deaths: {0} (Last 45 Days)'.format(selected_country),
            xaxis={'type': 'date', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=300, legend=dict(x=.2, y=-.15, orientation='h'))

        trace_3 = [go.Bar(name='Daily Recoveries', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Recovered_Diff'].tail(45), marker_color='#009E73', opacity=0.6),
        go.Scatter(name='5 Day Moving Average', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Recovered_Diff'].tail(45).rolling(window=5).mean(), mode='lines', line=dict(color='#009E73', width = 3))]
        layout_t3 = go.Layout(yaxis={'title': 'Number of Recovered', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Daily Recovered: {0} (Last 45 Days)'.format(selected_country),
            xaxis={'type': 'date', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=300, legend=dict(x=.2, y=-.15, orientation='h'))

        return vals,final_df.loc[(final_df['Date'] == final_df['Date'].max()) & (final_df['Country_Region'] == selected_country), 'Confirmed_Diff'],{'data':trace_1, 'layout': layout_t1},final_df.loc[(final_df['Date'] == final_df['Date'].max()) & (final_df['Country_Region'] == selected_country), 'Deaths_Diff'],{'data':trace_2, 'layout':layout_t2},final_df.loc[(final_df['Date'] == final_df['Date'].max()) & (final_df['Country_Region'] == selected_country), 'Recovered_Diff'],{'data':trace_3, 'layout':layout_t3}
    

    else:
        options = ['Confirmed','Recovered','Deaths', 'Total and Daily Confirmed Cases']

        vals = [{'label': i, 'value': i} for i in options]

        trace_1 = [go.Bar(name='Daily Cases', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Confirmed_Diff'].tail(45), marker_color='#648FFF', opacity=0.6),
        go.Scatter(name='5 Day Moving Average', x = final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Confirmed_Diff'].tail(45).rolling(window=5).mean(), mode='lines', line=dict(color='#648FFF', width = 3))]
        layout_t1 = go.Layout(yaxis={'title': 'Number of Confirmed Cases', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Daily Confirmed Cases: {0} (Last 45 Days)'.format(selected_country),
            xaxis={'type': 'date', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=300, legend=dict(x=.2, y=-.15, orientation='h'))

        trace_2 = [go.Bar(name='Daily Deaths', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Deaths_Diff'].tail(45), marker_color='#DC267F', opacity=0.6),
        go.Scatter(name='5 Day Moving Average', x = final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Deaths_Diff'].tail(45).rolling(window=5).mean(), mode='lines', line=dict(color='#DC267F', width = 3))]
        layout_t2 = go.Layout(yaxis={'title': 'Number of Deaths', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Daily Deaths: {0} (Last 45 Days)'.format(selected_country),
            xaxis={'type': 'date', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=300, legend=dict(x=.2, y=-.15, orientation='h'))

        trace_3 = [go.Bar(name='Daily Recoveries', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Recovered_Diff'].tail(45), marker_color='#009E73', opacity=0.6),
        go.Scatter(name='5 Day Moving Average', x=final_df.loc[(final_df['Country_Region'] == selected_country),'Date'].tail(45), y=final_df.loc[(final_df['Country_Region'] == selected_country),'Recovered_Diff'].tail(45).rolling(window=5).mean(), mode='lines', line=dict(color='#009E73', width = 3))]
        layout_t3 = go.Layout(yaxis={'title': 'Number of Recovered', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Daily Recovered: {0} (Last 45 Days)'.format(selected_country),
            xaxis={'type': 'date', 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'}, height=300, legend=dict(x=.2, y=-.15, orientation='h'))

        return vals,final_df.loc[(final_df['Date'] == final_df['Date'].max()) & (final_df['Country_Region'] == selected_country), 'Confirmed_Diff'],{'data':trace_1, 'layout': layout_t1},final_df.loc[(final_df['Date'] == final_df['Date'].max()) & (final_df['Country_Region'] == selected_country), 'Deaths_Diff'],{'data':trace_2, 'layout':layout_t2},final_df.loc[(final_df['Date'] == final_df['Date'].max()) & (final_df['Country_Region'] == selected_country), 'Recovered_Diff'],{'data':trace_3, 'layout':layout_t3}



@app.callback(
    Output(component_id='box-1',component_property='figure'),
    [Input(component_id='main-dropdown', component_property = 'value'),
    Input(component_id='main-dropdown-2', component_property = 'value')])

def update_maingraph(selected_country, selected_graph):
    if selected_graph is None and selected_country is None:

        selected_country = 'Canada'

        figmain_t = [go.Bar(name='Total Confirmed Cases', x=final_df.loc[(final_df['Country_Region'] == selected_country) ,'Date'], y = final_df.loc[(final_df['Country_Region'] == selected_country) ,'Confirmed'], marker_color='#648FFF')]
        figmain_l = go.Layout(yaxis={'title': 'Number of Cases', 'range':[0, (final_df.loc[(final_df['Country_Region'] == selected_country) ,'Confirmed'].max() * 1.10)], 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Overall Progression of COVID-19: {0}'.format(str(selected_country)),
            hovermode='x unified', xaxis=dict(title='Date', fixedrange=True, automargin=True, showline=True, mirror=False, linewidth=2, linecolor='black'))

        return {'data':figmain_t, 'layout': figmain_l}

    elif selected_graph is None and selected_country is not None:

        figmain_t = [go.Bar(name='Total Confirmed Cases', x=final_df.loc[(final_df['Country_Region'] == selected_country) ,'Date'], y = final_df.loc[(final_df['Country_Region'] == selected_country) ,'Confirmed'], marker_color='#648FFF')]
        figmain_l = go.Layout(yaxis={'title': 'Number of Cases', 'range':[0, (final_df.loc[(final_df['Country_Region'] == selected_country) ,'Confirmed'].max() * 1.10)], 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Overall Progression of COVID-19: {0}'.format(str(selected_country)),
            hovermode='x unified', xaxis=dict(title='Date', fixedrange=True, automargin=True, showline=True, mirror=False, linewidth=2, linecolor='black'))

        return {'data':figmain_t, 'layout': figmain_l}

    elif selected_graph == 'Total and Daily Confirmed Cases':
        figmain_t = [go.Scatter(name='Total Confirmed Cases', x=final_df.loc[(final_df['Country_Region'] == selected_country) ,'Date'], y = final_df.loc[(final_df['Country_Region'] == selected_country) ,'Confirmed'], line=dict(color='#1A85FF', width = 1.5), mode='lines'),
        go.Scatter(name='Daily Confirmed Cases', x=final_df.loc[(final_df['Country_Region'] == selected_country) ,'Date'], y=final_df.loc[(final_df['Country_Region'] == selected_country),'Confirmed_Diff'], line=dict(color='#D41159', width = 3), mode='lines', fill='tozeroy')]
        figmain_l = go.Layout(yaxis={'title': 'Number of Cases', 'range':[0, (final_df.loc[(final_df['Country_Region'] == selected_country) ,'Confirmed'].max() * 1.10)], 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Overall Progression of COVID-19 ({0}): {1}'.format(str(selected_country), str(selected_graph)),
            hovermode='x unified', xaxis=dict(title='Date',fixedrange=True, automargin=True, showline=True, mirror=False, linewidth=2, linecolor='black'))

        return {'data':figmain_t, 'layout': figmain_l}

    else:
        cols_dict = {'Confirmed':'#648FFF', 'Deaths':'#DC267F', 'Recovered':'#009E73'}

        figmain_t = [go.Bar(name='Total {0}'.format(selected_graph), x=final_df.loc[(final_df['Country_Region'] == selected_country) ,'Date'], y = final_df.loc[(final_df['Country_Region'] == selected_country) ,selected_graph], marker_color=cols_dict[selected_graph])]
        figmain_l = go.Layout(yaxis={'title': 'Number of Cases', 'range':[0, (final_df.loc[(final_df['Country_Region'] == selected_country) ,selected_graph].max() * 1.10)], 'automargin': True, 'showline':True, 'mirror':False, 'linewidth':2, 'linecolor':'black'},
            title='Overall Progression of COVID-19 ({0}): {1}'.format(str(selected_country), str(selected_graph)),
            hovermode='x unified', xaxis=dict(title='Date', fixedrange=True, automargin=True, showline=True, mirror=False, linewidth=2, linecolor='black'))

        return {'data':figmain_t, 'layout': figmain_l}


if __name__ == '__main__':
    app.run_server()