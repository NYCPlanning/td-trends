import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=pd.read_csv(path+'hubbound/transit/hubbound.csv')
dfcolors={'PATH':'rgba(237,102,93,0.8)',
          'NJT':'rgba(114,158,206,0.8)',
          'LIRR':'rgba(168,120,110,0.8)',
          'MNR':'rgba(103,191,92,0.8)',
          'Amtrak':'rgba(237,151,202,0.8)',
          'NJ Bus':'rgba(109,204,218,0.8)'}


fig=go.Figure()
fig=fig.add_trace(go.Scattergl(name='',
                               mode='none',
                               x=df['Year'],
                               y=df['Amtrak'],
                               showlegend=False,
                               hovertext=['<b>Year: </b>'+str(x) for x in df['Year']],
                               hoverinfo='text'))
for i in ['PATH','NJT','LIRR','MNR','Amtrak','NJ Bus']:
    fig=fig.add_trace(go.Scattergl(name=i,
                                   mode='lines+markers',
                                   x=df['Year'],
                                   y=df[i],
                                   line={'color':dfcolors[i],
                                         'width':2},
                                   marker = {'color': dfcolors[i],
                                             'size': 6},
                                   hovertext=['<b>'+str(i)+': </b>'+'{:,.0f}'.format(x) for x in df[i]],
                                   hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Daily Entries into the Manhattan Hub</b>',
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
    yaxis={'title':{'text':'<b>Daily Entries</b>',
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
    text='Data Source: <a href="https://www.nymtc.org/Data-and-Modeling/Transportation-Data-and-Statistics/Publications/Hub-Bound-Travel" target="blank">NYMTC Hub Bound Travel </a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/hubbound/transit/hubbound.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)
fig.write_html(path+'hubbound/transit/hubbound.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})















