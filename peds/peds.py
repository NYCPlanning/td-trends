import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'


# Bi-Annual Ped Counts
df=pd.read_csv(path+'peds/pedcounts.csv')
dfcolors={'AM':'rgba(114,158,206,0.8)',
          'PM':'rgba(255,158,74,0.8)',
          'Sat':'rgba(103,191,92,0.8)'}
fig=go.Figure()
fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=df['Year'],
                             y=df['May AM'],
                             showlegend=False,
                             hovertext=['<b>Year: </b>'+str(x) for x in df['Year']],
                             hoverinfo='text'))
for i in ['AM','PM','Sat']:
    fig=fig.add_trace(go.Scatter(name='May '+i,
                                 mode='lines+markers',
                                 x=df['Year'],
                                 y=df['May '+i],
                                 line={'color':dfcolors[i],
                                       'width':2},
                                 marker = {'color':dfcolors[i],
                                           'size':4},
                                 hovertext=['<b>May '+str(i)+': </b>'+'{:,.0f}'.format(x) for x in df['May '+i]],
                                 hoverinfo='text'))
    fig=fig.add_trace(go.Scatter(name='Sept '+i,
                                 mode='lines+markers',
                                 x=df['Year'],
                                 y=df['Sept '+i],
                                 line={'color':dfcolors[i],
                                       'width':2,
                                       'dash':'dot'},
                                 marker = {'color': dfcolors[i],
                                           'size':4},
                                 hovertext=['<b>Sept '+str(i)+': </b>'+'{:,.0f}'.format(x) for x in df['Sept '+i]],
                                 hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Average Peak Hour Pedestrian Counts*</b>',
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
           'dtick':'M12',
           'range':[min(df['Year'])-0.5,max(df['Year'])+0.5],
           'fixedrange':True,
           'showgrid':False},
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
    text='*AM: Weekday 7-9AM; PM: Weekday 4-7PM; Sat: Saturday 12-2PM',
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
    text='Data Source: <a href="https://www1.nyc.gov/html/dot/html/about/datafeeds.shtml#Pedestrians" target="blank">NYC DOT</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/peds/pedcounts.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-100)
fig.write_html(path+'peds/pedcounts.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})






# Times Square Ped Counts
df=pd.read_csv(path+'peds/timessquare.csv')
dfcolors={'AM':'rgba(114,158,206,0.8)',
          'PM':'rgba(255,158,74,0.8)',
          'Sat':'rgba(103,191,92,0.8)'}
fig=go.Figure()
fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=df['Year'],
                             y=df['May AM'],
                             showlegend=False,
                             hovertext=['<b>Year: </b>'+str(x) for x in df['Year']],
                             hoverinfo='text'))
for i in ['AM','PM','Sat']:
    fig=fig.add_trace(go.Scatter(name='May '+i,
                                 mode='lines+markers',
                                 x=df['Year'],
                                 y=df['May '+i],
                                 line={'color':dfcolors[i],
                                       'width':2},
                                 marker = {'color':dfcolors[i],
                                           'size':4},
                                 hovertext=['<b>May '+str(i)+': </b>'+'{:,.0f}'.format(x) for x in df['May '+i]],
                                 hoverinfo='text'))
    fig=fig.add_trace(go.Scatter(name='Sept '+i,
                                 mode='lines+markers',
                                 x=df['Year'],
                                 y=df['Sept '+i],
                                 line={'color':dfcolors[i],
                                       'width':2,
                                       'dash':'dot'},
                                 marker = {'color': dfcolors[i],
                                           'size':4},
                                 hovertext=['<b>Sept '+str(i)+': </b>'+'{:,.0f}'.format(x) for x in df['Sept '+i]],
                                 hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Average Peak Hour Pedestrian Counts*</b>',
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
           'dtick':'M12',
           'range':[min(df['Year'])-0.5,max(df['Year'])+0.5],
           'fixedrange':True,
           'showgrid':False},
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
    text='*AM: Weekday 7-9AM; PM: Weekday 4-7PM; Sat: Saturday 12-2PM',
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
    text='Data Source: <a href="https://www1.nyc.gov/html/dot/html/about/datafeeds.shtml#Pedestrians" target="blank">NYC DOT</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/peds/pedcounts.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-100)
fig.write_html(path+'peds/pedcounts.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})