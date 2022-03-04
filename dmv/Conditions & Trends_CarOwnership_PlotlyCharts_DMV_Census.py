# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 11:07:32 2021

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


rawdf =pd.read_csv(path+'DMV_Vehicle_Registrations_Census.csv', header = 0)
meltdf = rawdf
meltdf['County'] = meltdf['County'].str.lower().str.title()
meltdf.loc[meltdf['County']=="Nyc", "County"] = "NYC"
meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>% Change Population: </b>'+meltdf['% Change Population'].map('{:,.2%}'.format)+'<br><b>% Change NYS Vehicle Registration: </b>'+meltdf['% Change NYS Vehicle Registration'].map('{:,.2%}'.format)
#meltdf['HOVER']='<b>County: </b>'
#meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>Vehicle: </b>'+meltdf['Vehicle']


fig=go.Figure()

fig = go.Figure(data=[
    go.Bar(name='% Change Population', x=meltdf['County'], y=meltdf['% Change Population'], marker_color='#729ece', hoverinfo='text', hovertext=meltdf['HOVER'], text=meltdf['% Change Population'].map('{:.2%}'.format), textposition='outside'),
    go.Bar(name='% Change NYS Vehicle Registration', x=meltdf['County'], y=meltdf['% Change NYS Vehicle Registration'], marker_color='#ff9e4a', hoverinfo='text', hovertext=meltdf['HOVER'], text=meltdf['% Change NYS Vehicle Registration'].map('{:.2%}'.format), textposition='outside')
])




fig.update_layout(
    barmode='group',
#    barnorm='number',
    template='plotly_white',
    title={'text':'<b>Percent Change in NYS DMV Standard Vehicle Registrations (2010-2018) vs<br>Census Population (2010-2020), by Borough</b>',
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
    text='Data Source: <a href="https://dmv.ny.gov/about-dmv/statistical-summaries" target="blank">NYS DMV Statistical Summary</a> | <a href="https://www1.nyc.gov/site/planning/planning-level/nyc-population/2020-census.page" target="blank">Census Population Summary</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/test/test.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=-0.1,
    yanchor='top',
    yref='paper')

fig.write_html(path+'DMV_Vehicle_Registrations_Census.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})