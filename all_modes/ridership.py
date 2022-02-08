# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update
Source: See Excel Notes
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

path = 'C:/Users/M_Free/Desktop/td-trends/all_modes/annotations/'

df = pd.read_csv(path + 'ridership_annual.csv')
df_total = df[['year', 'ridership']].groupby('year').sum().reset_index()
df_total.columns = ['year', 'total']
df = pd.merge(df, df_total, how = 'inner', on = 'year')
df['%'] = df['ridership'] / df['total']
df['hover'] = '<i>' + df['mode'] + ': </i>' + df['ridership'].map('{:,.0f}'.format) + ' (' + df['%'].map('{:.0%}'.format) + ')'

df_total['year'] = df_total['year'].astype(str)
df_total['y'] = [0 for i in range(df_total['year'].size)]

mode_colors = {'Subway': '#729ece',
               'Bus': '#67bf5c',
               'Commuter Rail': '#ff9e4a',               
               'Taxi': '#ed665d',
               'For Hire Vehicle': '#ad8bc9',
               'Ferry': '#6dccda',             
               'Citi Bike': '#ed97ca'}


fig = go.Figure()

for mode, color in mode_colors.items():
    fig = fig.add_trace(go.Scatter(name = mode,
                                   x = df.loc[df['mode'] == mode, 'year'],
                                   y = df.loc[df['mode'] == mode, 'ridership'],
                                   mode = 'lines+markers',
                                   line = {'color': color,
                                           'width': 2},
                                   hoverinfo = 'text',
                                   hovertext = df.loc[df['mode'] == mode, 'hover']))

fig = fig.add_trace(go.Scatter(x = df_total['year'],
                               y = df_total['y'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = '<b>' + df_total['year'] + ' Total Ridership: ' + df_total['total'].map('{:,.0f}'.format)))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Annual Ridership by Mode</b>',
                           'font_size': 20,
                           'x': 0.5,
                           'xanchor':'center',
                           'y': 0.95,
                           'yanchor': 'top'},
                  legend = {'orientation': 'h',
                            'title_text': '',
                            'font_size': 16,
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120,
                            'l': 80,
                            'r': 80,
                            't': 120},
                  xaxis = {'title': {'text': '<b>Year</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'dtick': 'M12',
                           'range': [min(df['year'])-0.5, max(df['year'])+0.5],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Ridership</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'fixedrange': True,
                           'showgrid': True},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False,
                  hovermode = 'x unified',
                  hoverlabel = {'font_size': 14})

fig.add_annotation(text = '<a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/all_modes/annotations/ridership_annual.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False,
                   x = 1,
                   xanchor = 'right',
                   xref = 'paper',
                   y = -0.1,
                   yanchor = 'top',
                   yref = 'paper')

fig

# fig.write_html(path + 'ridership_annual.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/all_modes/annotations/annual_ridership.html')   