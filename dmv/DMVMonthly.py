import pandas as pd
import datetime
import plotly.io as pio
import plotly.graph_objects as go



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=pd.read_csv(path+'dmv/DMVMonthly.csv')
df['Date']=[datetime.datetime.strptime(str(x)+'01','%Y%m%d') for x in df['YearMonth']]



fig=go.Figure()
fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=df['Date'],
                             y=df['Counts'],
                             showlegend=False,
                             hovertext=['<b>Month: </b>'+datetime.datetime.strftime(x,'%b %Y') for x in df['Date']],
                             hoverinfo='text'))
fig=fig.add_trace(go.Bar(name='Counts',
                         x=df['Date'],
                         y=df['Counts'],
                         showlegend=False,
                         marker={'color':'rgba(109,204,218,0.8)'},
                         hovertext=['<b>Vehicle Registrations: </b>'+'{:,.0f}'.format(x) for x in df['Counts']],
                         hoverinfo='text'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>NYS Standard Vehicle Monthly Registrations</b><br>(Excluding Revocation and Suspension)',
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
    margin={'b':160,
            'l':80,
            'r':40,
            't':120},
    xaxis={'title':{'text':'<b>Month</b>',
                    'font_size':14},
           'tickfont_size':12,
           'tickformat':'%b %Y',
           'dtick':'M2',
           'range':[min(df['Date'])-datetime.timedelta(days=15),max(df['Date'])+datetime.timedelta(days=15)],
           'fixedrange':True,
           'showgrid':False},
    yaxis={'title':{'text':'<b>Number of Vehicles</b>',
                    'font_size':14},
           'tickfont_size':12,
           'range':[1500000,2000000],
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False,
    hovermode='x unified')
fig.add_annotation(
    text='Data Source: <a href="https://data.ny.gov/Transportation/Vehicle-Snowmobile-and-Boat-Registrations/w4pv-hbkt" target="blank">NYS DMV</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/dmv/DMVMonthly.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-120)
fig.write_html(path+'dmv/DMVMonthly.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})



