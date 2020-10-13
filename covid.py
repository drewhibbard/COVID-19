#!/Users/drewhibbard/anaconda3/bin/python3

'''
Module for scraping coronavirus table from worldometer.info
'''
import requests
from bs4 import BeautifulSoup
import pickle
import numpy as np
import pandas as pd


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


def get_us_info():
    url = 'https://www.worldometers.info/coronavirus/country/us/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,features='lxml')

    table = soup.find('tbody')

    headers = ['num','state','total_cases','new_cases','total_deaths','new_deaths','total_recovered',
        'active_cases','cases_per_m','deaths_per_m','total_tests','tests_per_m','population',
            'source','projections']

    rows = [row for row in table.find_all('tr')]
    states = []

    for row in rows[1:]:
        items = row.find_all('td')
        info = [item.text for item in items]
        final = dict(zip(headers,info))
        states.append(final)

    covid = pd.DataFrame(states)
    covid.drop(['source','projections','num'],axis=1,inplace=True)
    
    for col in covid.columns:
        covid[col] = covid[col].str.replace('\n','')

    covid.replace('N/A',0,inplace=True)
    covid.replace(' ',0,inplace=True)

    for col in ['total_cases','active_cases','cases_per_m','deaths_per_m','total_tests','tests_per_m','population']:
        covid[col] = covid[col].str.replace(',','')
        covid[col] = pd.to_numeric(covid[col])

    for col in ['new_cases','total_deaths','new_deaths','total_recovered']:
        covid[col] = covid[col].str.replace(',','')
        covid[col] = covid[col].str.replace('+','')
        covid[col] = pd.to_numeric(covid[col])

    with open('worldometer_us.pickle','wb') as to_write:
        pickle.dump(covid,to_write)


get_world_info()
get_us_info()