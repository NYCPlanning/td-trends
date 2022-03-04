# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 15:56:18 2022

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


rawdf =pd.read_csv(path+'DMV_Vehicle_Registrations_Monthly.csv', header = 0)
meltdf = rawdf

meltdf['HOVER']='<b>Month: </b>'+meltdf['Month']+'<br><b>Vehicle Registrations: </b>'+meltdf['Counts'].map('{:,.0f}'.format)
#meltdf['HOVER']='<b>County: </b>'
#meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>Vehicle: </b>'+meltdf['Vehicle']


fig=go.Figure()

fig = go.Figure(data=[
    go.Bar(name='Vehicle Registrations', x=meltdf['Month'], y=meltdf['Counts'], marker_color='#729ece', hoverinfo='text', hovertext=meltdf['HOVER'], text=meltdf['Counts'].map('{:,.0f}'.format), textposition='outside')],
           layout_yaxis_range=[1800000,2000000])




fig.update_layout(
    barmode='group',
#    barnorm='number',
    template='plotly_white',
    title={'text':'<b>DMV Standard Series Vehicle Registrations in NYC<br>Excluding Revocation and Suspension<br> Nov, 2019 - Dec 2021</b>',
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

fig.write_html(path+'DMV_Vehicle_Registrations_Monthly.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})

