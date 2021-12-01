# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Commutting 

Source: 2019 ACS 5-Year PUMS
Date: November 2021 
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.renderers.default = 'browser'

col_list = ['SERIALNO', 'ST', 'PUMA', 'PWGTP', 'POWPUMA','JWRIP','JWTRNS', 'JWMNP']

pums_ny = pd.read_csv('C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/csv_pny.csv', 
                      usecols=col_list, dtype={'SERIALNO': str})
pums_ct = pd.read_csv('C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/csv_pct.csv', 
                      usecols=col_list, dtype={'SERIALNO': str})
pums_nj = pd.read_csv('C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/csv_pnj.csv', 
                      usecols=col_list, dtype={'SERIALNO': str})
pums_pa = pd.read_csv('C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/csv_ppa.csv', 
                      usecols=col_list, dtype={'SERIALNO': str})

# assign puma codes for each boro 
bronx = list(range(3700,3711))
brooklyn = list(range(4000,4019))
manhattan = list(range(3800,3811))
queens = list(range(4100,4115))
si = list(range(3900,3904))
nyc = bronx + brooklyn + manhattan + queens + si

# COMMUTING FLOWS

nyc_commuters = pums_ny[pums_ny.PUMA.isin(nyc)]
nyc_commuters = nyc_commuters[nyc_commuters.POWPUMA.notna()] # github csv

regional_commuters = pd.concat([pums_ny, pums_ct, pums_nj, pums_pa])
regional_commuters = regional_commuters[~regional_commuters.PUMA.isin(nyc)]
regional_commuters = regional_commuters[regional_commuters.POWPUMA.isin(nyc)]  

live_nyc = nyc_commuters['PWGTP'].sum()
live_work_nyc = nyc_commuters[nyc_commuters.POWPUMA.isin(nyc)]['PWGTP'].sum()
work_nyc = live_work_nyc + regional_commuters['PWGTP'].sum()

# print('Workers Living in NYC: ' 
#       + str('{:,}'.format(live_nyc)))
# print('Workers Working in NYC: ' 
#       + str('{:,}'.format(work_nyc)))
# print('Workers Living & Working in NYC: ' 
#       + str('{:,}'.format(live_work_nyc)))
# print('Workers Living in NYC & Working Elsewhere: ' 
#       + str('{:,}'.format(live_nyc - live_work_nyc)))
# print('Workers Living Elsewhere & Working in NYC: '
#       + str('{:,}'.format(work_nyc - live_work_nyc)))

# NYC COMMUTERS: DESTINATION

nyc_commuters['RES'] = np.select([nyc_commuters.PUMA.isin(bronx),
                                  nyc_commuters.PUMA.isin(brooklyn),
                                  nyc_commuters.PUMA.isin(manhattan),
                                  nyc_commuters.PUMA.isin(queens),
                                  nyc_commuters.PUMA.isin(si)],
                                 ['Bronx',
                                  'Brooklyn',
                                  'Manhattan',
                                  'Queens',
                                  'Staten Island'])

nyc_commuters['POW'] = np.select([nyc_commuters.POWPUMA.isin(bronx), 
                                  nyc_commuters.POWPUMA.isin(brooklyn),
                                  nyc_commuters.POWPUMA.isin(manhattan), 
                                  nyc_commuters.POWPUMA.isin(queens),  
                                  nyc_commuters.POWPUMA.isin(si)],
                                 ['Bronx', 
                                  'Brooklyn', 
                                  'Manhattan', 
                                  'Queens', 
                                  'Staten Island'],
                                 default = 'Region')

nyc_commuters['DEST'] = np.select([nyc_commuters['POW'] == 'Region',
                                   nyc_commuters['RES'] == nyc_commuters['POW']],
                                  ['Region',
                                   'Same Boro'],
                                  default = 'Other Boro')

dest = nyc_commuters[['RES','DEST','PWGTP']].groupby(['RES', 'DEST']).sum().reset_index()

dest_fig = px.bar(dest, 
                  x = 'RES', 
                  y = 'PWGTP', 
                  color = 'DEST',
                  labels = {'RES':'<b>Residence<b>', 
                            'PWGTP':'<b>Number of Workers<b>', 
                            'DEST':'<b>Destination<b>'},
                  color_discrete_sequence= ['#729ece','#ff9e4a','#67bf5c'],     #EDIT
                  category_orders= {'DEST': ['Same Boro',
                                             'Other Boro',
                                             'Region']},
                  title = '<b>Destination of Work by Borough of Residence for NYC Commuters<b>')
dest_fig.show()

# NYC COMMUTERS: TRAVEL MODE

di = {2: 'Bus',
      3: 'Subway', 
      4: 'Rail',
      5: 'Rail',
      6: 'Other',
      7: 'Other',
      8: 'Other',
      9: 'Other',
      10: 'Other',
      11: 'Work From Home',
      12: 'Other'}

def get_mn(row):
    if np.isnan(row['JWRIP']) == True: 
        return di[row['JWTRNS']]
    elif row['JWRIP'] == 1: 
        return 'Drive Alone'
    else: 
        return 'Carpool'
    
nyc_commuters['TM'] = nyc_commuters.apply(get_mn, axis=1)

tm = nyc_commuters[['RES', 'TM', 'PWGTP']].groupby(['RES', 'TM']).sum()
tm['% TM'] = tm.div(tm.sum(level=0), level=0) 
tm = tm.reset_index()

tm_fig = px.bar(tm,
                x = 'RES',
                y = '% TM',
                color = 'TM',
                labels = {'RES': '<b>Residence<b>',
                          '% TM': '<b>Percentage<b>',
                          'TM' : '<b>Travel Mode<b>'},
                category_orders={'TM':['Subway', 
                                       'Rail', 
                                       'Bus',
                                       'Drive Alone', 
                                       'Carpool', 
                                       'Other', 
                                       'Work From Home']},
                title = '<b>Travel Mode to Work by Borough of Residence for NYC Commuters<b>')
tm_fig.update_layout(yaxis_tickformat = '.1%')
tm_fig.show()

# determine mode split for commuters not living or working in manhattan
tm_not_mn = nyc_commuters[['RES', 'POW', 'TM', 'PWGTP']].groupby(['RES','POW','TM']).sum()
tm_not_mn = tm_not_mn.drop(index='Manhattan')
tm_not_mn = tm_not_mn.drop(index='Manhattan', level =1).reset_index()
tm_not_mn = tm_not_mn.groupby(['TM']).sum().reset_index()

sorter = ['Subway','Rail','Bus','Drive Alone','Carpool', 'Other', 'Work From Home']
tm_not_mn = tm_not_mn.set_index('TM').loc[sorter].reset_index()


fig = go.Figure()

fig = fig.add_pie(values = tm_not_mn['PWGTP'],
                  labels = tm_not_mn['TM'],
                  direction = 'clockwise', 
                  showlegend = True,
                  sort = False,
                  textfont = {'family':'Arial'},
                  title = 'Mode Split for Commuters Living or Working in the Outer Boroughs')
fig.show()

tm_not_mn_fig = px.pie(tm_not_mn, 
                       values = 'PWGTP',
                       names = 'TM',
                       labels = {'TM':'Travel Mode', 
                                 'PWGTP':'Number of Workers'}, 
                       title = '<b>Mode Split of NYC Commuters Living or Working in the Outer Boroughs<b>')
tm_not_mn_fig.show()

# NYC COMMUTERS: TRAVEL TIME

nyc_commuters['MN'] = np.select([nyc_commuters['POW'] == 'Manhattan'],
                                ['Manhattan Bound'], 
                                default='Non-Manhattan Bound')

nyc_commuters['TT'] = np.select([nyc_commuters['JWMNP'] < 30, 
                                 nyc_commuters['JWMNP'] < 60],
                                ['Less Than 30 Mins', 
                                 '30 to 60 Mins'],
                                default='More Than 60 Mins')

tt = nyc_commuters[['RES', 'DEST', 'TT', 'PWGTP']].groupby(['RES', 'DEST', 'TT']).sum().reset_index()

tt_fig = px.bar(tt, 
                x = 'RES', 
                y = 'PWGTP', 
                color = 'TT',
                facet_col = 'DEST',
                labels = {'RES':'Residence', 
                          'PWGTP':'Number of Workers', 
                          'DEST':'Destination', 
                          'TT':'Travel Time'},
                category_orders={'TT': ['Less Than 30 Mins',
                                        '30 to 60 Mins', 
                                        'More Than 60 Mins'], 
                                 'DEST':['Same Boro',
                                         'Other Boro',
                                         'Region']},
                title = 'Travel Time to Destination of Work by Borough of Residence for NYC Commuters')
tt_fig.show()

# determine travel time by manhattan or non-manhattan destinations
tt_mn = nyc_commuters[['MN','TT', 'PWGTP']].groupby(['MN', 'TT']).sum()
tt_mn['% MN'] = tt_mn.div(tt_mn.sum(level=0), level=0)
tt_mn = tt_mn.reset_index()

tt_mn_fig = px.bar(tt_mn, 
                   x='MN', 
                   y='% MN', 
                   color='TT', 
                   labels = {'MN': 'Place of Work',
                             '% MN': 'Percentage',
                             'TT': 'Travel Time'},
                   category_orders={'TT': ['Less Than 30 Mins',
                                           '30 to 60 Mins', 
                                           'More Than 60 Mins']},
                   title = 'Travel Time by Place of Work for NYC Commuters')
tt_mn_fig.update_layout(yaxis_tickformat = '.1%')
tt_mn_fig.show()

# REGIONAL IN-COMMUTERS: DESTINATION

regional_commuters['RES'] = np.select([regional_commuters['ST'] == 36,
                                       regional_commuters['ST'] == 9,
                                       regional_commuters['ST'] == 34,
                                       regional_commuters['ST'] == 42],
                                      ['New York',
                                       'Connecticut',
                                       'New Jersey',
                                       'Pennsylvania'])

regional_commuters['POW'] = np.select([regional_commuters.POWPUMA.isin(bronx),
                                       regional_commuters.POWPUMA.isin(brooklyn),
                                       regional_commuters.POWPUMA.isin(manhattan),
                                       regional_commuters.POWPUMA.isin(si),
                                       regional_commuters.POWPUMA.isin(queens)],
                                      ['Bronx',
                                       'Brooklyn',
                                       'Manhattan',
                                       'Staten Island',
                                       'Queens'])

dest_rc = regional_commuters[['RES','POW', 'PWGTP']].groupby(['RES', 'POW']).sum().reset_index()
dest_rc 

boro_colors = {'Bronx': '#729ece',
               'Brooklyn': '#ff9e4a',
               'Manhattan': '#67bf5c',
               'Staten Island': '#ed665d',
               'Queens': '#ad8bc9'}

fig = go.Figure()

for i in ['Bronx', 'Brooklyn', 'Manhattan', 'Staten Island', 'Queens']:
    fig = fig.add_trace(go.Bar(name = i,
                               x = '<b>'+ dest_rc.loc[dest_rc['POW'] == i, 'RES']+'<b>',
                               y = dest_rc.loc[dest_rc['POW'] == i, 'PWGTP'],
                               marker = {'color': boro_colors[i]},
                               width = .5))

fig.update_layout(
    barmode='stack',
    template='plotly_white',
    title={'text':'<b>Destination of Work by State for Regional In-Commuters</b>',
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
    xaxis={'categoryorder': 'total descending',
           'tickfont_size':14,
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

fig                 
                               
regional_commuters


