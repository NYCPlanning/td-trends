# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Biking

Source(s): NYC DOHMH Community Health Survey 2020
Date: December 2021 
"""
import pyreadstat
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'
path = '/Users/Work/Desktop/GitHub/td-trends/bike/annotations/'

# CYCLISTS

local_path = '/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/chs2020_public.sas7bdat' 
cols = ['cyclingfreq', 'wt21_dual']
chs, meta = pyreadstat.read_sas7bdat(local_path, usecols=cols)

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

# BIKE COUNTS

# CITI BIKE