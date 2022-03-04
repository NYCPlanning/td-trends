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


rawdf =pd.read_csv(path+'ACS_Vehicle_Availability.csv', header = 0)

rawdf1 = rawdf[['County', '# No vehicle', '# 1 vehicle', '# 2 vehicles', '# 3 or more vehicles']]
meltdf1 = rawdf1.melt(id_vars="County", value_name="Household")
meltdf1["Vehicle"] = meltdf1["variable"].str[2:]
meltdf1 = meltdf1.drop(columns="variable")

rawdf2 = rawdf[['County', '% No vehicle', '% 1 vehicle', '% 2 vehicles', '% 3 or more vehicles']]
meltdf2 = rawdf2.melt(id_vars="County", value_name="Percent")
meltdf2["Vehicle"] = meltdf2["variable"].str[2:]
meltdf2 = meltdf2.drop(columns="variable")

meltdf = pd.merge(meltdf1, meltdf2, left_on = ["County", "Vehicle"], right_on = ["County", "Vehicle"], how="left")

meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>Vehicle: </b>'+meltdf['Vehicle']+'<br><b>Number of Households: </b>'+meltdf['Household'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+meltdf['Percent'].map('{:.0%}'.format)
#meltdf['HOVER']='<b>County: </b>'
#meltdf['HOVER']='<b>County: </b>'+meltdf['County']+'<br><b>Vehicle: </b>'+meltdf['Vehicle']

dfcolors={'No vehicle':'#729ece',
          '1 vehicle':'#cdcc5d',
          '2 vehicles':'#a2a2a2',
          '3 or more vehicles':'#ed97ca'}

fig=go.Figure()
for i in ['No vehicle', '1 vehicle', '2 vehicles', '3 or more vehicles']:
    fig=fig.add_trace(go.Bar(name=i,
                             x='<b>'+meltdf.loc[meltdf['Vehicle']==i,'County']+'</b>',
                             y=meltdf.loc[meltdf['Vehicle']==i,'Percent'],
                             marker={'color':dfcolors[i]},
                             text=meltdf.loc[meltdf['Vehicle']==i,'Percent'].map('{:.0%}'.format),
                             textposition='inside',
                             width=0.5,
                             hoverinfo='text',
                             hovertext=meltdf.loc[meltdf['Vehicle']==i,'HOVER']))
fig.update_layout(
    barmode='stack',
    barnorm='percent',
    template='plotly_white',
    title={'text':'<b>Vehicles Kept at Home for NYC Households</b>',
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
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False)

fig.add_annotation(
    text='Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/test/test.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=-0.1,
    yanchor='top',
    yref='paper')

fig.write_html(path+'ACS_Vehicle_Availability.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})