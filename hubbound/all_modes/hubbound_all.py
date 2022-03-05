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

# path = '/Users/Work/Desktop/GitHub/td-trends/hubbound/all_modes/'
path = 'C:/Users/M_Free/Desktop/td-trends/hubbound/all_modes/'
path = 'C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/hubbound/all_modes/'

df = pd.read_csv(path + 'hubbound_all.csv')
df['hover'] = '<i>' + df['mode'] + ': </i>' + df['entries'].map('{:,.0f}'.format) + ' (' + df['%'].map('{:.0%}'.format) + ')'

df_total = df[['year', 'entries']].groupby('year').sum().reset_index()
df_total['year'] = df_total['year'].astype(str)
df_total['y'] = [0 for i in range(df_total['year'].size)]

mode_colors = {'Auto': 'rgba(237,102,93,0.8)',
               'Subway': 'rgba(114,158,206,0.8)',
               'Rail': 'rgba(168,120,110,0.8)',
               'Bus': 'rgba(103,191,92,0.8)',
               'Other': 'rgba(237,151,202,0.8)'}

fig = go.Figure()

for mode, color in mode_colors.items():
    fig = fig.add_trace(go.Scatter(name = mode,
                                   x = df.loc[df['mode'] == mode, 'year'],
                                   y = df.loc[df['mode'] == mode, 'entries'],
                                   mode = 'lines+markers',
                                   line = {'color': color,
                                           'width': 2},
                                   marker = {'color': color,
                                             'size': 6},                                   
                                   hoverinfo = 'text',
                                   hovertext = df.loc[df['mode'] == mode, 'hover']))

fig = fig.add_trace(go.Scatter(x = df_total['year'],
                               y = df_total['y'],
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
                            'r': 40,
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
                           'rangemode': 'tozero',
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
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -80)

fig

# fig.write_html(path + 'annotations/entries.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/hubbound/all_modes/annotations/entries.html')   
