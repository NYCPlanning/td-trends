import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import datetime



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'


# Bi-Annual Ped Counts
df=pd.read_csv(path+'ped/pedcounts.csv')
dfcolors={'Weekday AM Peak':'rgba(255,158,74,0.8)',
          'Weekday PM Peak':'rgba(173,139,201,0.8)',
          'Saturday Midday':'rgba(103,191,92,0.8)'}
fig=go.Figure()
fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=list(range(0,len(df))),
                             y=df['Weekday AM Peak'],
                             showlegend=False,
                             hovertext=['<b>Year: </b>'+str(x) for x in df['Year']],
                             hoverinfo='text'))
for i in ['Weekday AM Peak','Weekday PM Peak','Saturday Midday']:
    fig=fig.add_trace(go.Scatter(name=i,
                                 mode='lines+markers',
                                 x=list(range(0,len(df))),
                                 y=df[i],
                                 line={'color':dfcolors[i],
                                       'width':2},
                                 marker = {'color': dfcolors[i],
                                           'size': 6},
                                 hovertext=['<b>'+str(i)+': </b>'+'{:,.0f}'.format(x) for x in df[i]],
                                 hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Average Peak Hour Pedestrian Counts</b>',
           'font_size':20,
           'x':0.5,
           'xanchor':'center',
           'y':0.95,
           'yanchor':'top'},
    legend={'orientation':'h',
            'title_text':'',
            'font_size':16,
            'x':0.5,
            'xanchor':'center',
            'y':1,
            'yanchor':'bottom'},
    margin={'b':120,
            'l':80,
            'r':40,
            't':120},
    xaxis={'title':{'text':'<b>Year</b>',
                    'font_size':14},
           'tickfont_size':12,
           'tickvals':list(range(0,len(df))),
           'ticktext':df['Year'],
           'tickmode':'array',
           'range':[-0.5,len(df)-0.5],
           'fixedrange':True,
           'showgrid':False,
           'zeroline':False},
    yaxis={'title':{'text':'<b>Hourly Total</b>',
                    'font_size':14},
           'tickfont_size':12,
           'rangemode':'tozero',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False,
    hovermode='x unified')
fig.add_annotation(
    text='<i>*Spring Only; **Fall Only</i>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)
fig.add_annotation(
    text='Data Source: <a href="https://data.ny.gov/Transportation/Bi-Annual-Pedestrian-Counts/2de2-6x2h/about" target="blank">NYC DOT</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/ped/pedcounts.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-100)
fig.write_html(path+'ped/pedcounts.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})






# Times Square Ped Counts
df=pd.read_csv(path+'ped/timessquare.csv')
df['Date']=[datetime.datetime.strptime(str(x)+'01','%Y%m%d') for x in df['YearMonth']]

fig=go.Figure()
fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=df['Date'],
                             y=df['PedCounts'],
                             showlegend=False,
                             hovertext=['<b>Month: </b>'+datetime.datetime.strftime(x,'%b %Y') for x in df['Date']],
                             hoverinfo='text'))
fig=fig.add_trace(go.Bar(name='PedCounts',
                         x=df['Date'],
                         y=df['PedCounts'],
                         showlegend=False,
                         marker={'color':'rgba(114,158,206,0.8)'},
                         hovertext=['<b>Counts: </b>'+'{:,.0f}'.format(x) for x in df['PedCounts']],
                         hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Times Square Average Daily Visitors</b>',
           'font_size':20,
           'x':0.5,
           'xanchor':'center',
           'y':0.95,
           'yanchor':'top'},
    legend={'orientation':'h',
            'title_text':'',
            'font_size':16,
            'x':0.5,
            'xanchor':'center',
            'y':1,
            'yanchor':'bottom'},
    margin={'b':100,
            'l':80,
            'r':40,
            't':60},
    xaxis={'title':{'text':'<b>Month</b>',
                    'font_size':14},
           'tickfont_size':12,
           'tickformat':'%b %Y',
           'dtick':'M2',
           'range':[min(df['Date'])-datetime.timedelta(days=15),max(df['Date'])+datetime.timedelta(days=15)],
           'fixedrange':True,
           'showgrid':False},
    yaxis={'title':{'text':'<b>Counts</b>',
                    'font_size':14},
           'tickfont_size':12,
           'rangemode':'tozero',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False,
    hovermode='x unified')
fig.add_annotation(
    text='Data Source: <a href="https://www.timessquarenyc.org/do-business/market-research-data/pedestrian-counts" target="blank">Times Square Alliance</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/ped/timessquare.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)
fig.write_html(path+'ped/timessquare.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})