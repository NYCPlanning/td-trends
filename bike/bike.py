# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Biking

Source(s): NYC DOHMH Community Health Survey 2020
Date: December 2021 - January 2022 
"""
import pyreadstat
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
import numpy as np

pio.renderers.default = 'browser'
path = 'C:/Users/M_Free/Desktop/td-trends/bike/annotations/'
# path = '/Users/Work/Desktop/GitHub/td-trends/bike/annotations/'
local_path = 'C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/'
# local_path = '/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/' 

#%% CYCLISTS

cols = ['cyclingfreq', 'wt21_dual']
chs, meta = pyreadstat.read_sas7bdat(local_path + 'chs2020_public.sas7bdat', usecols=cols)

chs = chs.groupby(['cyclingfreq']).sum().reset_index()

# combine never and unable to bike 
var = chs['wt21_dual'][4] + chs['wt21_dual'][5]
chs = chs.append({'cyclingfreq': 7, 'wt21_dual': var}, ignore_index = True)
chs = chs.drop(labels = [4,5], axis = 0)

chs['%'] = chs['wt21_dual'] / chs['wt21_dual'].sum()

chs = chs.replace({1:'Once a Week or More',
                   2:'Several Times a Month',
                   3:'At Least Once a Month',
                   4:'A Few Times a Year',
                   7:'Never or Unable'})

# chs.to_csv(path + 'chs.csv',index=False)

chs['hover'] = '<b>Frequency: </b>'+ chs['cyclingfreq'] + '<br><b>Adults: </b>' + chs['wt21_dual'].map('{:,.0f}'.format) +'<br><b>Percentage: </b>' + chs['%'].map('{:.0%}'.format)

chs_colors = {'Once a Week or More': '#729ece',
              'Several Times a Month': '#ff9e4a',
              'At Least Once a Month': '#67bf5c',
              'A Few Times a Year': '#ed665d',
              'Never or Unable': 'a5acaf'}
                
fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = chs['cyclingfreq'],
                           values = chs['%'],
                           hole = .5,
                           sort = False,
                           direction = 'clockwise',
                           marker = {'colors': list(chs_colors.values())},
                           textinfo = 'none',
                           hoverinfo = 'text',
                           hovertext = chs['hover']))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Adult New Yorkers Who Ride a Bike<b>',
                           'font_size': 20,
                           'x': .5,
                           'xanchor': 'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'font_size': 16,
                            'x': .5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www1.nyc.gov/site/doh/data/data-sets/community-health-survey-public-use-data.page" target="blank">NYC DOHMH Community Health Survey 2020</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/chs.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')

fig.add_annotation(text = f'N = {chs["wt21_dual"].sum():,.0f}',
                   font_size = 14,
                   showarrow = False, 
                   x = .5,
                   y = .5)
                  
fig 

# fig.write_html(path + 'chs.html', include_plotlyjs='cdn', config={'displayModeBar':False})
# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/chs.html')

#%% BIKE COUNTS

parser = lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p')
counts = pd.read_csv(local_path + 'bicycle_counts.csv', parse_dates = ['date'], date_parser = parser)
counters = pd.read_csv(local_path + 'bicycle_counters.csv')

# counts.merge(counters, on= 'id', how = 'left')

# test = counters.set_index('id').to_dict()['name']

# for i in range(len(counts)):
#     if counts['id'][i] in test:
#         counts['test'][i] = test[counts['id'][i]]


# counts['test'] = counts['id'].apply(lambda x: x.map(test))

# counts['test'] = counts['id'].map(test)

# MN Bridge 100010022 (overall vs. bk and mn bound)
# SI Ferry 100010017
# Queensboro 100009428
# Williamsburg 100009427
# Kent Ave
# 1st Ave at 26th St
# Prospect Park West
# Pulaski Bridge
# 8th Ave at 50th St
# Broadway at 50th t
# Amsterdam Ave at 86th St
# Columbus Ave at 96th St

# https://medium.com/qri-io/which-nyc-bridge-has-the-most-bike-traffic-6bb291eb74ef

#%% CITI BIKE

citibike = pd.read_csv(path + 'citibike.csv')
citibike['12M Rolling Avg'] = citibike['Avg Daily Rides'].rolling(window = 12).mean()
citibike['Hover'] = '<b>Date: </b>' + citibike['Date2']+'<br><b>Average Daily Rides: </b>' + citibike['Avg Daily Rides'].map('{:,.0f}'.format) + '<br><b>12-Month Rolling Average: </b>' + citibike['12M Rolling Avg'].map('{:,.0f}'.format)

fig = go.Figure()

fig = fig.add_trace(go.Bar(x = citibike['Date'],
                           y = citibike['Avg Daily Rides'],
                           marker = {'color': '#729ece'},
                           name = 'Average Daily Rides',
                           hoverinfo = 'text', 
                           hovertext = citibike['Hover']))

fig = fig.add_trace(go.Scatter(x = citibike['Date'],
                               y = citibike['12M Rolling Avg'], 
                               marker = {'color': '#ff9e4a'},
                               name = '12-Month Rolling Average',
                               mode = 'lines',
                               hoverinfo = 'none'))
    
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Citi Bike Operations<b>',
                           'font_size': 20,
                           'x': .5,
                           'xanchor': 'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'font_size': 16,
                            'x': .5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120},
                  xaxis = {'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'tickfont_size': 12,
                           'rangemode': 'nonnegative',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://ride.citibikenyc.com/system-data/operating-reports" target="blank">Citi Bike Monthly Operating Reports</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/annotations/citibike.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
fig

# fig.write_html(path + 'citibike.html', include_plotlyjs='cdn', config={'displayModeBar':False})
# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/citibike.html')

