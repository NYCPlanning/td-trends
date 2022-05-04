import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import datetime

pio.renderers.default = 'browser'
pd.set_option('display.max_columns', None)

path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/economy/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/economy/'


cat_colors = {'NYC Office Jobs': 'rgba(237,102,93,0.8)',
               'NYC Non-Office Jobs': 'rgba(255,158,74,0.8)',
               'Office Usage': 'rgba(103,191,92,0.8)',             
               'Times Square Pedestrian Counts': 'rgba(173,139,201,0.8)',
               'Subway Ridership':'rgba(114,158,206,0.8)'}

df = pd.read_csv(path + 'economy.csv')
df['Date']=[datetime.datetime.strptime(str(x)+'-01','%Y-%m-%d') for x in df['YearMonth']]


fig = go.Figure()

fig = fig.add_trace(go.Scatter(x = df['Date'],
                               y = df['Office Usage'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = ['<b>Month: </b>' + datetime.datetime.strftime(x,'%b %Y') for x in df['Date']]))

for cat, color in cat_colors.items():
    fig = fig.add_trace(go.Scatter(name = cat,
                                   x = df['Date'],
                                   y = df[cat],
                                   mode = 'lines+markers',
                                   line = {'color': color,
                                           'width': 2},
                                   marker = {'color': color,
                                             'size': 6},    
                                   hoverinfo = 'text',
                                   hovertext = ['<b>'+cat+': </b>'+'{:.0%}'.format(x) for x in df[cat]]))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Monthly Economic Trends During Pandemic</b>',
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
                            't': 120},
                  xaxis = {'title': {'text': '<b>Month</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'dtick': 'M2',
                           'range':[min(df['Date'])-datetime.timedelta(days=15),max(df['Date'])+datetime.timedelta(days=15)],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Percent of Pre-Pandemic Baseline</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'tickformat': '.0%',
                           'rangemode':'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False,
                  hovermode = 'x unified',
                  hoverlabel = {'bgcolor':'rgba(255,255,255,0.95)',
                                'bordercolor':'rgba(0,0,0,0.1)',
                                'font_size': 14})

fig.add_annotation(text = 'Data Source: <a href="https://dol.ny.gov/current-employment-statistics-0">NYS Department of Labor</a>; <a href="https://www.kastle.com/">Kastle Systems</a>; <a href="https://www.timessquarenyc.org/do-business/market-research-data/pedestrian-counts">Times Square Alliance</a>; <a href="https://new.mta.info/coronavirus/ridership">MTA</a>',
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

fig.write_html(path + 'economy.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})

