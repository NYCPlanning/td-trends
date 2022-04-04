import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

pio.renderers.default = 'browser'

path = 'C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/micromobility/'
path = 'C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/micromobility/'

df=pd.read_csv(path+'micromobility.csv')
df['hover'] = '<b>Type: </b>'+ df['Type'] + '<br><b>Counts: </b>' + df['Counts'].map('{:,.0f}'.format) +'<br><b>Percentage: </b>' + df['Pct'].map('{:.0%}'.format)

dfcolors = {'E-Bikes': 'rgba(237,102,93,0.8)',
            'E-Scooters': 'rgba(255,158,74,0.8)',
            'Other Micromobility': 'rgba(173,139,201,0.8)',
            'Manual Bikes': 'rgba(114,158,206,0.8)'}

fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = df['Type'],
                           values = df['Pct'],
                           hole = 0.5,
                           sort = False,
                           direction = 'clockwise',
                           pull=0.05,
                           marker = {'colors': list(dfcolors.values())},
                           textinfo = 'text',
                           text= df['Pct'].map('{:.0%}'.format),
                           textposition='outside',
                           textfont={'size':14},
                           hoverinfo = 'text',
                           hovertext = df['hover']))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Micromobility Peak Hour Sample Counts<b>',
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
                  margin = {'b': 40, 
                            'l': 80,
                            'r': 80,
                            't': 200},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: NYC DCP (2021) | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/micromobility/micromobility.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y=0,
                   yanchor='top',
                   yref='paper',
                   yshift=0)
                  
fig

fig.write_html(path + 'micromobility.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False})

# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/chs.html')

