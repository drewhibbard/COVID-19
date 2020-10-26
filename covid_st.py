import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.write('''
# Interactive Visualizations of COVID-19''')


us = pd.read_csv('https://api.covidtracking.com/v1/states/daily.csv')
us.date = pd.to_datetime(us.date,format='%Y%m%d')

us.sort_values(by=['state','date'],inplace=True)
us.reset_index(inplace=True)
us.date = us.date.dt.date

us = us[us.date>pd.to_datetime('03-05-2020')]

us['cases_daily'] = us.positive.diff()
us['tests_daily'] = us.totalTestResults.diff()

us.loc[us.cases_daily<0,'cases_daily'] = 0
us.loc[us.tests_daily<0,'tests_daily'] = 0
us['percent_positive'] = us.cases_daily/us.tests_daily


metric = st.selectbox('Choose metric',['positive','totalTestResults','hospitalizedCurrently','inIcuCurrently',
                                      'onVentilatorCurrently','recovered','cases_daily','test_daily','percent_positive'])

fig = px.choropleth(us,locations='state',locationmode='USA-states',
               color=metric,hover_name='state',
               color_continuous_scale='sunsetdark',
               hover_data=['deathIncrease','hospitalizedCurrently'])

fig.update_layout(title=metric + ' over time',title_x=0.5)

    


#fig = map_metric_over_time(us,metric)
st.plotly_chart(fig)