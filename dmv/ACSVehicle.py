import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'


#%% Annual
df=pd.read_csv(path+'dmv/ACSAnnual.csv')
dfcolors={'Bronx':'rgba(114,158,206,0.8)',
          'Brooklyn':'rgba(255,158,74,0.8)',
          'Manhattan':'rgba(103,191,92,0.8)',
          'Queens':'rgba(237,102,93,0.8)',
          'Staten Island':'rgba(173,139,201,0.8)',
          'NYC Population':'rgba(168,120,110,0.8)'}

fig=go.Figure()

fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=df['Year'],
                             y=df['Manhattan'],
                             showlegend=False,
                             hovertext=['<b>Year: </b>'+str(x) for x in df['Year']],
                             hoverinfo='text'))
for i in ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']:
    fig=fig.add_trace(go.Scatter(name=i,
                                 mode='lines+markers',
                                 x=df['Year'],
                                 y=df[i],
                                 line={'color':dfcolors[i],
                                       'width':2},
                                 marker={'color': dfcolors[i],
                                         'size': 6},
                             hovertext=['<b>'+str(i)+': </b>'+'{:,.0f}'.format(x)+' ('+'{:,.0%}'.format(y)+')' for x,y in zip(df[i],df[i+' Pct'])],
                             hoverinfo='text'))
fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=df['Year'],
                             y=df['Manhattan'],
                             showlegend=False,
                             hovertext=['<b>Total Vehicles: </b>'+'{:,.0f}'.format(x) for x in df['Total Vehicles']],
                             hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Total Vehicles Available</b>',
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
            't':160},
    xaxis={'title':{'text':'<b>Year</b>',
                    'font_size':14},
           'tickfont_size':12,
           'dtick':'M12',
           'range':[min(df['Year'])-0.5,max(df['Year'])+0.5],
           'fixedrange':True,
           'showgrid':False},
    yaxis={'title':{'text':'<b>Number of Vehicles</b>',
                    'font_size':14},
           'tickfont_size':12,
           'rangemode':'tozero',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'bgcolor':'rgba(255,255,255,0.95)',
                'bordercolor':'rgba(0,0,0,0.1)',
                'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False,
    hovermode='x unified')
fig.add_annotation(
    text='Data Source: <a href="https://data.census.gov/cedsci/table?t=Transportation&g=0500000US36005,36047,36061,36081,36085&tid=ACSDT1Y2019.B25046" target="blank">Census Bureau ACS 1-Year</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/dmv/ACSAnnual.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)
fig.write_html(path+'dmv/ACSAnnual.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})






#%% Ratio
df=pd.read_csv(path+'dmv/ACSRatio.csv')

dfcolors={'No Vehicle':'rgba(114,158,206,0.8)',
          '1 Vehicle':'rgba(103,191,92,0.8)',
          '2 Vehicles':'rgba(255,158,74,0.8)',
          '3 or More Vehicles':'rgba(237,102,93,0.8)'}

fig=go.Figure()

for i in ['3 or More Vehicles','2 Vehicles','1 Vehicle','No Vehicle']:
    fig=fig.add_trace(go.Bar(name=i,
                             x=['<b>'+str(x)+'</b><br>'+'{:.2f}'.format(y)+'<br>Veh/HH' for x,y in zip(df['Boro'],df['Ratio'])],
                             y=df[str(i)+' Pct'],
                             marker={'color': dfcolors[i]},
                             width=0.5,
                             hovertext=['<b>Borough: </b>'+str(x)+'<br><b>'+str(i)+': </b>'+'{:,.0f}'.format(y)+'<br><b>Percentage: </b>'+'{:,.0%}'.format(z) for x,y,z in zip(df['Boro'],df[i],df[i+' Pct'])],
                             hoverinfo='text'))
fig.update_layout(
    barmode = 'stack',
    template='plotly_white',
    title={'text':'<b>Households by Vehicle Availability</b>',
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
    xaxis={'tickfont_size':14,
           'fixedrange':True,
           'showgrid':False},
    yaxis={'title':{'text':'<b>Percent of Households</b>',
                    'font_size':14},
           'tickfont_size':12,
           'tickformat': ',.0%',
           'rangemode':'tozero',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False)
fig.add_annotation(
    text='Data Source: <a href="https://data.census.gov/cedsci/table?t=Transportation&g=0500000US36005,36047,36061,36081,36085&tid=ACSDT5Y2020.B25044" target="blank">Census Bureau 2019 ACS 1-Year</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/dmv/ACSRatio.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)
fig.write_html(path+'dmv/ACSRatio.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})
