import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=pd.read_csv(path+'dmv/DMVAnnual.csv')
dfcolors={'Bronx':'rgba(114,158,206,0.8)',
          'Brooklyn':'rgba(255,158,74,0.8)',
          'Manhattan':'rgba(103,191,92,0.8)',
          'Queens':'rgba(237,102,93,0.8)',
          'Staten Island':'rgba(173,139,201,0.8)',
          'NYC Population':'rgba(168,120,110,0.8)'}



fig=go.Figure()
fig=fig.add_trace(go.Scattergl(name='NYC Population',
                               mode='lines+markers',
                               x=df['Year'],
                               y=df['NYC Population'],
                               yaxis='y2',
                               line={'color':dfcolors['NYC Population'],
                                     'width':3},
                               marker = {'color': dfcolors['NYC Population'],
                                         'size': 8},
                               hovertext=['<b>NYC Population: </b>'+'{:,.0f}'.format(x) for x in df['NYC Population']],
                               hoverinfo='text'))
fig=fig.add_trace(go.Scattergl(name='',
                               mode='none',
                               x=df['Year'],
                               y=df['Manhattan'],
                               showlegend=False,
                               hovertext=['<b>Total Vehicles: </b>'+'{:,.0f}'.format(x) for x in df['Total Vehicles']],
                               hoverinfo='text'))
for i in ['Staten Island','Queens','Manhattan','Brooklyn','Bronx']:
    fig=fig.add_trace(go.Bar(name=i,
                             x=df['Year'],
                             y=df[i],
                             marker={'color': dfcolors[i]},
                             width=0.5,
                             hovertext=['<b>'+str(i)+': </b>'+'{:,.0f}'.format(x)+' ('+'{:,.0%}'.format(y)+')' for x,y in zip(df[i],df[i+' Pct'])],
                             hoverinfo='text'))
fig=fig.add_trace(go.Scattergl(name='',
                               mode='none',
                               x=df['Year'],
                               y=df['Manhattan'],
                               showlegend=False,
                               hovertext=['<b>Year: </b>'+str(x) for x in df['Year']],
                               hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>NYS Standard Vehicle Annual Registrations</b>',
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
            'r':80,
            't':150},
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
    yaxis2={'title':{'text':'<b>NYC Population</b>',
                     'font_size':14},
            'tickfont_size':12,
            'side':'right',
            'overlaying':'y',
            'rangemode':'tozero',
            'fixedrange':True,
            'showgrid':False},
    barmode='stack',             
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False,
    hovermode='x unified')
fig.add_annotation(
    text='Data Source: <a href="https://dmv.ny.gov/about-dmv/statistical-summaries" target="blank">NYS DMV</a>; <a href="https://data.census.gov/cedsci/table?t=Populations%20and%20People&g=0500000US36005,36047,36061,36081,36085&d=ACS%201-Year%20Estimates%20Data%20Profiles&tid=ACSDP1Y2019.DP05" target="blank">Census Bureau</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/dmv/DMVAnnual.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)
fig.write_html(path+'dmv/DMVAnnual.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})



