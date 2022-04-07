# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update
Source: See Excel Notes (TD Trends: All Modes: Ridership)
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import datetime

pio.renderers.default = 'browser'

path = 'C:/Users/M_Free/Desktop/td-trends/all_modes/annotations/'
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/all_modes/annotations/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/all_modes/annotations/'



#%% Annual Ridership

mode_colors = {'Subway': 'rgba(114,158,206,0.8)',
               'Bus': 'rgba(103,191,92,0.8)',
               'Ferry': 'rgba(237,151,202,0.8)',             
               'Commuter Rail': 'rgba(168,120,110,0.8)',               
               'Bridges & Tunnels': 'rgba(173,139,201,0.8)',
               'Taxi': 'rgba(255,158,74,0.8)',
               'For-Hire Vehicle': 'rgba(237,102,93,0.8)',
               'Citi Bike': 'rgba(109,204,218,0.8)',
               'Airport': 'rgba(205,204,93,0.8)'}

mode_notes={'Subway': '*',
            'Bus': '*',
            'Ferry': '*',             
            'Commuter Rail': '*',    
            'Bridges & Tunnels': '**',
            'Taxi': '***',
            'For-Hire Vehicle': '***',
            'Citi Bike': '***',
            'Airport': '*'}

df = pd.read_csv(path + 'ridership_annual.csv')
# df_total = df[['date', 'ridership']].groupby('date').sum().reset_index()
# df_total.columns = ['date', 'total']
# df = pd.merge(df, df_total, how = 'inner', on = 'date')
# df['%'] = df['ridership'] / df['total']
# df['hover'] = '<i>' + df['mode'] + ': </i>' + df['ridership'].map('{:,.0f}'.format) + ' (' + df['%'].map('{:.0%}'.format) + ')'
# df_total['date'] = df_total['date'].astype(str)
# df_total['y'] = [0 for i in range(df_total['date'].size)]
df['hover'] = '<b>' + df['Mode'] + ': </b>' + df['Value'].map('{:,.0f}'.format)

fig = go.Figure()

fig = fig.add_trace(go.Scatter(x = df.loc[df['Mode'] == 'Citi Bike', 'Year'],
                               y = df.loc[df['Mode'] == 'Citi Bike', 'Value'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = ['<b>Year: </b>' + str(x) for x in df.loc[df['Mode'] == 'Citi Bike', 'Year']]))

for mode, color in mode_colors.items():
    fig = fig.add_trace(go.Scatter(name = mode+mode_notes[mode],
                                   x = df.loc[df['Mode'] == mode, 'Year'],
                                   y = df.loc[df['Mode'] == mode, 'Value'],
                                   mode = 'lines+markers',
                                   line = {'color': color,
                                           'width': 2},
                                   marker = {'color': color,
                                             'size': 6},    
                                   hoverinfo = 'text',
                                   hovertext = df.loc[df['Mode'] == mode, 'hover']))

# fig = fig.add_trace(go.Scatter(x = df_total['date'],
#                                y = df_total['y'],
#                                mode = 'none',
#                                showlegend = False,
#                                hoverinfo = 'text',
#                                hovertext = '<b>Total Ridership: ' + df_total['total'].map('{:,.0f}'.format)))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Annual Trends by Mode</b>',
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
                  margin = {'b': 140,
                            'l': 80,
                            'r': 40,
                            't': 160},
                  xaxis = {'title': {'text': '<b>Year</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'dtick': 'M12',
                           'range': [min(df['Year'])-0.5, max(df['Year'])+0.5],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Ridership / Vehicles / Trips</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'rangemode': 'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False,
                  hovermode = 'x unified',
                  hoverlabel = {'bgcolor':'rgba(255,255,255,0.95)',
                                'bordercolor':'rgba(0,0,0,0.1)',
                                'font_size': 14})

fig.add_annotation(text = '<i>*Ridership; **Vehicles (MTA & PANYNJ Only); ***Trips</i>',
                    font_size = 14,
                    showarrow = False,
                    x = 1,
                    xanchor = 'right',
                    xref = 'paper',
                    y = 0,
                    yanchor = 'top',
                    yref = 'paper',
                    yshift = -80)

fig.add_annotation(text = 'Data Source: <a href="https://github.com/NYCPlanning/td-trends/raw/main/all_modes/annotations/data_source.xlsx" target="blank">MTA; NYC DOT; NYC TLC; Citi Bike; PANYNJ</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/all_modes/annotations/ridership_annual.csv" target="blank">Download Chart Data</a>',
                    font_size = 14,
                    showarrow = False,
                    x = 1,
                    xanchor = 'right',
                    xref = 'paper',
                    y = 0,
                    yanchor = 'top',
                    yref = 'paper',
                    yshift = -100)

fig

fig.write_html(path + 'ridership_annual.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})

# https://nycplanning.github.io/td-trends/all_modes/annotations/annual_ridership.html')   

#%% Monthly Ridership as % of 2019 
mode_colors = {'Subway': 'rgba(114,158,206,0.8)',
               'Bus': 'rgba(103,191,92,0.8)',
               'Ferry': 'rgba(237,151,202,0.8)',             
               'Commuter Rail': 'rgba(168,120,110,0.8)',               
               'Bridges & Tunnels': 'rgba(173,139,201,0.8)',
               'Taxi': 'rgba(255,158,74,0.8)',
               'For-Hire Vehicle': 'rgba(237,102,93,0.8)',
               'Citi Bike': 'rgba(109,204,218,0.8)',
               'Airport': 'rgba(205,204,93,0.8)'}

mode_notes={'Subway': '*',
            'Bus': '*',
            'Ferry': '*',             
            'Commuter Rail': '*',    
            'Bridges & Tunnels': '**',
            'Taxi': '***',
            'For-Hire Vehicle': '***',
            'Citi Bike': '***',
            'Airport': '*'}

df = pd.read_csv(path + 'ridership_covid.csv')
# df_total = df[['date', 'ridership']].groupby('date').sum().reset_index()
# df_total.columns = ['date', 'total']
df['hover'] = '<b>' + df['Mode'] + ': </b>' + df['% of 2019'].map('{:.0%}'.format) + ' (' + df['Value'].map('{:,.0f}'.format) + ')'
#df_total['date'] = df_total['date'].astype(str)
# df_total['y'] = [0 for i in range(df_total['date'].size)]
df['YearMonth']=[datetime.datetime.strptime(str(x)+'-01','%Y-%m-%d') for x in df['YearMonth']]

fig = go.Figure()

fig = fig.add_trace(go.Scatter(x = df.loc[df['Mode'] == 'Commuter Rail', 'YearMonth'],
                               y = df.loc[df['Mode'] == 'Commuter Rail', '% of 2019'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = ['<b>Month: </b>' + datetime.datetime.strftime(x,'%b %Y') for x in df.loc[df['Mode'] == 'Commuter Rail', 'YearMonth']]))

for mode, color in mode_colors.items():
    fig = fig.add_trace(go.Scatter(name = mode+mode_notes[mode],
                                   x = df.loc[df['Mode'] == mode, 'YearMonth'],
                                   y = df.loc[df['Mode'] == mode, '% of 2019'],
                                   mode = 'lines+markers',
                                   line = {'color': color,
                                           'width': 2},
                                   marker = {'color': color,
                                             'size': 6},    
                                   hoverinfo = 'text',
                                   hovertext = df.loc[df['Mode'] == mode, 'hover']))

# fig = fig.add_trace(go.Scatter(x = df_total['date'],
#                                y = df_total['y'],
#                                mode = 'none',
#                                showlegend = False,
#                                hoverinfo = 'text',
#                                hovertext = '<b>Total Ridership: ' + df_total['total'].map('{:,.0f}'.format)))

fig = fig.add_trace(go.Bar(name='Positive Cases',
                           x = df.loc[df['Mode'] == 'Positive Cases', 'YearMonth'],
                           y = df.loc[df['Mode'] == 'Positive Cases', 'Value'],
                           yaxis='y2',
                           showlegend = True,
                           marker={'color':'rgba(162,162,162,0.4)'},
                           hoverinfo = 'text',
                           hovertext = ['<b>Positive Cases: </b>'+'{:,.0f}'.format(x)  for x in df.loc[df['Mode'] == 'Positive Cases', 'Value']]))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Monthly Trends by Mode During Pandemic</b>',
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
                  margin = {'b': 140,
                            'l': 80,
                            'r': 40,
                            't': 160},
                  xaxis = {'title': {'text': '<b>Month</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'dtick': 'M2',
                           'range':[min(df['YearMonth'])-datetime.timedelta(days=15),max(df['YearMonth'])+datetime.timedelta(days=15)],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Percent of 2019</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'tickformat': '.0%',
                           'side':'left',
                           'overlaying':'y2',
                           'range':[0,1.9],
                           'fixedrange': True,
                           'showgrid': True},
                  yaxis2 = {'title':{'text': '<b>Cases</b>',
                                    'font_size': 14,
                                    'font_color':'rgba(162,162,162,1)'},
                           'tickfont':{'size': 12,
                                       'color':'rgba(162,162,162,1)'},
                           'side':'right',
                           'range':[0,550000],
                           'fixedrange': True,
                           'showgrid': False},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False,
                  hovermode = 'x unified',
                  hoverlabel = {'bgcolor':'rgba(255,255,255,0.95)',
                                'bordercolor':'rgba(0,0,0,0.1)',
                                'font_size': 14})

fig.add_annotation(text = '<i>*Ridership; **Vehicles (MTA & PANYNJ Only); ***Trips</i>',
                    font_size = 14,
                    showarrow = False,
                    x = 1,
                    xanchor = 'right',
                    xref = 'paper',
                    y = 0,
                    yanchor = 'top',
                    yref = 'paper',
                    yshift = -80)

fig.add_annotation(text = 'Data Source: <a href="https://github.com/NYCPlanning/td-trends/raw/main/all_modes/annotations/data_source.xlsx" target="blank">MTA; NYC DOT; NYC TLC; Citi Bike; PANYNJ; NYC DOHMH</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/all_modes/annotations/ridership_annual.csv" target="blank">Download Chart Data</a>',
                    font_size = 14,
                    showarrow = False,
                    x = 1,
                    xanchor = 'right',
                    xref = 'paper',
                    y = 0,
                    yanchor = 'top',
                    yref = 'paper',
                    yshift = -100)

fig

fig.write_html(path + 'ridership_covid.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})

# https://nycplanning.github.io/td-trends/all_modes/annotations/ridership_covid.html')   