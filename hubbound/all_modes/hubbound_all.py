#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Entries to the CBD

Source: NYMTC Hub Bound Travel 2019
Date: November - December 2021 
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

# path = '/Users/Work/Desktop/GitHub/td-trends/hubbound/all_modes/'
path = 'C:/Users/M_Free/Desktop/td-trends/hubbound/all_modes/'

df = pd.read_csv(path + 'hubbound_all.csv', index_col = [0,1])

mode_colors = {'Auto': '#ed665d',
               'Bus': '#67bf5c',
               'Subway': '#729ece',
               'Rail': '#ff9e4a',
               'Other': '#ed97ca'}

# ENTRIES BY MODE

df_entries = df.loc[slice(None), 'Entries', :].reset_index().drop('Type', axis = 1)

fig = go.Figure()

for mode, color in mode_colors.items(): 
    fig = fig.add_trace(go.Scattergl(name = mode,
                                     mode = 'lines+markers',
                                     x = df_entries['Year'],
                                     y = df_entries[mode],
                                     line = {'color': color,
                                             'width': 2},
                                     hovertemplate = '%{y:,.0f}'))

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
                           'range': [min(df_entries['Year'])-0.5, max(df_entries['Year'])+0.5],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Daily Entries</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'rangemode': 'nonnegative',
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

# fig.write_html(path + 'annotations/commuters.html',
#                 include_plotlyjs = 'cdn',
#                 config = {'displayModeBar': False})

print('Chart Available at: https://nycplanning.github.io/td-trends/hubbound/all_modes/annotations/entries.html')  

# MODE SPLIT

df_pct = df.loc[slice(None), '%', :].reset_index().drop('Type', axis = 1)

fig = go.Figure()

for mode, color in mode_colors.items(): 
    
    
    fig.add_trace(go.Scatter(name = mode,
                             x = df_pct['Year'],
                             y = df_pct[mode],
                             mode = 'lines',
                             line = {'color': color,
                                     'width': .5},
                             stackgroup = 'one',
                             hovertemplate = '%{y:.0%}'))
    
fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Mode Split for Daily Entries into the Manhattan Hub</b>',
                           'font_size': 20,
                           'x': 0.5,
                           'xanchor':'center',
                           'y': 0.95,
                           'yanchor': 'top'},
                  legend = {'orientation': 'h',
                            'traceorder': 'normal',
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
                           'range': [min(df_pct['Year'])-0.5, max(df_pct['Year'])+0.5],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Percent of Total Daily Entries</b>',
                                    'font_size': 14},
                           'tickformat': ',.0%',
                           'tickfont_size': 12,
                           'rangemode': 'nonnegative',
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

# fig.write_html(path + 'annotations/mode_split.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

print('Chart Available at: https://nycplanning.github.io/td-trends/hubbound/all_modes/annotations/mode_split.html')   