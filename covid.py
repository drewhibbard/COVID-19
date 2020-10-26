#!/Users/drewhibbard/anaconda3/bin/python3

'''
Module for scraping coronavirus table from worldometer.info
'''
import requests
from bs4 import BeautifulSoup
import pickle
import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def get_world_info():
    url = 'https://www.worldometers.info/coronavirus/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,features='lxml')

    table = soup.find('tbody')

    headers = ['num','country','total_cases','new_cases','total_deaths','new_deaths','total_recovered',
           'scrap','active_cases','critical','cases_per_m','deaths_per_m','total_tests','tests_per_m','population']

    rows = [row for row in table.find_all('tr')]
    countries = []

    for row in rows[8:]:
        items = row.find_all('td')
        info = [item.text for item in items]
        final = dict(zip(headers,info))
        countries.append(final)

    covid = pd.DataFrame(countries)

    covid.replace('N/A',0,inplace=True)
    covid.replace(' ',0,inplace=True)

    for col in ['total_cases','active_cases','cases_per_m','deaths_per_m','total_tests','tests_per_m','population']:
        covid[col] = covid[col].str.replace(',','')
        covid[col] = pd.to_numeric(covid[col])

    for col in ['new_cases','total_deaths','new_deaths','total_recovered','critical']:
        covid[col] = covid[col].str.replace(',','')
        covid[col] = covid[col].str.replace('+','')
        covid[col] = pd.to_numeric(covid[col])

    covid.drop(['num','scrap'],axis=1,inplace=True)

    with open('worldometer_world.pickle','wb') as to_write:
        pickle.dump(covid,to_write)


def plot_stats(df,state):
    '''
    Input a two-letter state abbreviation as a string.  Ex: "CA"
    Returns: 3x2 subplots of coronavirus data:
        Daily Cases
        Daily Deaths
        Currently Hospitalized
        Currently on ICU
        Currently on Ventilator
        Percent of tests positive
    '''
    
    data = df[df.state==state]

    fig = make_subplots(rows=3,cols=2,subplot_titles=('Daily Cases','Daily Deaths',
                                                     'Hospitalized','ICU',
                                                     'On Ventilator','Percent of Tests Positive'))

    fig.add_trace(go.Scatter(x=data.date,y=data.cases_daily),row=1,col=1)

    fig.add_trace(go.Scatter(x=data.date,y=data.deathIncrease),row=1,col=2)

    fig.add_trace(go.Scatter(x=data.date,y=data.hospitalizedCurrently),row=2,col=1)

    fig.add_trace(go.Scatter(x=data.date,y=data.inIcuCurrently),row=2,col=2)

    fig.add_trace(go.Scatter(x=data.date,y=data.onVentilatorCurrently),row=3,col=1)

    fig.add_trace(go.Scatter(x=data.date,y=data.percent_positive),row=3,col=2)
    
    fig.update_layout(height=600, width=800,
                  title_text=state,title_x=0.5)

    fig.show()


def map_metric_over_time(df,metric):
    '''
    Expects a string equal to a column name.  Options include:
        positive (cumulative cases)
        totalTestResults (cumulative)
        hospitalizedCurrently
        inIcuCurrently
        onVentilatorCurrently
        recovered (cumulative)
        cases_daily
        test_daily
        percent_positive
    '''
    
    fig = px.choropleth(df,locations='state',locationmode='USA-states',
                   color=metric,hover_name='state',
                   color_continuous_scale='sunsetdark',
                   hover_data=['deathIncrease','hospitalizedCurrently'],
                   animation_frame='date_string')

    fig.update_layout(title=metric + ' over time',title_x=0.5)
    fig.show()


get_world_info()