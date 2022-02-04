#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Entries to the CBD
Source: NYMTC Hub Bound Travel
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

path = '/Users/Work/Desktop/GitHub/td-trends/hubbound/all_modes/'
# path = 'C:/Users/M_Free/Desktop/td-trends/hubbound/all_modes/'

df = pd.read_csv(path + 'hubbound_all.csv')
df['hover'] = '<i>' + df['mode'] + ': </i>' + df['entries'].map('{:,.0f}'.format) + ' (' + df['%'].map('{:.0%}'.format) + ')'

df_total = df[['year', 'entries']].groupby('year').sum().reset_index()
df_total['year'] = df_total['year'].astype(str)

mode_colors = {'Subway': '#729ece',
               'Auto': '#ed665d',
               'Rail': '#ff9e4a',
               'Bus': '#67bf5c',
               'Other': '#ed97ca'}

fig = go.Figure()

for mode, color in mode_colors.items():
    fig = fig.add_trace(go.Scatter(name = mode,
                                   x = df.loc[df['mode'] == mode, 'year'],
                                   y = df.loc[df['mode'] == mode, 'entries'],
                                   mode = 'lines+markers',
                                   line = {'color': color,
                                           'width': 2},
                                   hoverinfo = 'text',
                                   hovertext = df.loc[df['mode'] == mode, 'hover']))

fig = fig.add_trace(go.Scatter(x = df_total['year'],
                               y = df_total['entries'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = '<b>' + df_total['year'] + ' Total Entries: ' + df_total['entries'].map('{:,.0f}'.format)))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Daily Entries into the Manhattan Hub</b>',
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
                  yaxis = {'title':{'text': '<b>Daily Entries</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'range': [0, 2500000],
                           'fixedrange': True,
                           'showgrid': True},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False,
                  hovermode = 'x unified',
                  hoverlabel = {'font_size': 14})

fig.add_annotation(text = 'Data Source: <a href="https://www.nymtc.org/Data-and-Modeling/Transportation-Data-and-Statistics/Publications/Hub-Bound-Travel" target="blank">NYMTC Hub Bound Travel </a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/hubbound/all_modes/hubbound_all.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False,
                   x = 1,
                   xanchor = 'right',
                   xref = 'paper',
                   y = -0.1,
                   yanchor = 'top',
                   yref = 'paper')

fig

# fig.write_html(path + 'annotations/entries.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/hubbound/all_modes/annotations/entries.html')   
