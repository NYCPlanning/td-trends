# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 14:54:02 2021

@author: R_Lin
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

pio.renderers.default = 'browser'
pd.set_option('display.max_columns', None)
path='F:/Conditions & Trends/'


rawdf =pd.read_csv(path+'DMV_Vehicle_Registrations.csv', header = 0)
meltdf = rawdf
meltdf['County'] = meltdf['County'].str.lower().str.title()
meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>Year: </b>'+meltdf['Year'].apply(str)+'<br><b>DMV Vehicle Registrations: </b>'+meltdf['Vehicles'].map('{:,.0f}'.format)
#meltdf['HOVER']='<b>County: </b>'
#meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>Vehicle: </b>'+meltdf['Vehicle']

dfcolors={'Bronx':'#729ece',
          'Brooklyn':'#ff9e4a',
          'Manhattan':'#67bf5c',
          'Queens':'#ad8bc9',
          'Staten Island':'#ed665d'}

fig=go.Figure()
for i in ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']:
    fig=fig.add_trace(go.Bar(name=i,
                             x=meltdf.loc[meltdf['County']==i,'Year'],
                             y=meltdf.loc[meltdf['County']==i,'Vehicles'],
                             marker={'color':dfcolors[i]},
                             width=0.5,
                             hoverinfo='text',
                             hovertext=meltdf.loc[meltdf['County']==i,'HOVER']))
fig.update_layout(
    barmode='stack',
#    barnorm='number',
    template='plotly_white',
    title={'text':'<b>NYSDMV Standard Vehicle Registrations in NYC,<br>2010-2018</b>',
           'font_size':20,
           'x':0.5,
           'xanchor':'center',
           'y':0.95,
           'yanchor':'top'},
    legend={'traceorder':'normal',
            'orientation':'h',
            'title_text':'',
            'font_size':16,
            'x':0.5,
            'xanchor':'center',
            'y':1,
            'yanchor':'bottom'},
    margin={'b':120,
            'l':80,
            'r':80,
            't':120},
    xaxis={'tickfont_size':14,
           'fixedrange':True,
           'showgrid':False},
    yaxis={'tickfont_size':12,
           'rangemode':'nonnegative',
#           'autorange': True,
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False)

fig.add_annotation(
    text='Data Source: <a href="https://dmv.ny.gov/about-dmv/statistical-summaries" target="blank">NYS DMV Statistical Summary</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/test/test.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=-0.1,
    yanchor='top',
    yref='paper')

fig.write_html(path+'DMV_Vehicle_Registrations.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})