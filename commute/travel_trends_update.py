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

#path = 'C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/'
path = '/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/'

col_list = ['SERIALNO', 'ST', 'PUMA', 'PWGTP', 'POWPUMA','JWRIP','JWTRNS', 'JWMNP']

pums_ny = pd.read_csv(path + 'csv_pny.csv', usecols=col_list, dtype={'SERIALNO': str})
pums_ct = pd.read_csv(path + 'csv_pct.csv', usecols=col_list, dtype={'SERIALNO': str})
pums_nj = pd.read_csv(path + 'csv_pnj.csv', usecols=col_list, dtype={'SERIALNO': str})
pums_pa = pd.read_csv(path + 'csv_ppa.csv', usecols=col_list, dtype={'SERIALNO': str})

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
dest_total=dest[['RES','PWGTP']].groupby(['RES']).sum().reset_index()
dest_total.columns=['RES','TOTAL']
dest=pd.merge(dest,dest_total,how='inner',on='RES')
dest['% DEST']=dest['PWGTP']/dest['TOTAL']
dest.to_csv(path+'dest.csv',index=False)

dest['HOVER']='<b>Residence: </b>'+dest['RES']+'<br><b>Workplace: </b>'+dest['DEST']+'<br><b>Commuters: </b>'+dest['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest['% DEST'].map('{:.0%}'.format)

dest_colors = {'Same Boro':'#729ece',
               'Other Boro':'#ff9e4a',
               'Region':'#67bf5c'}

fig = go.Figure()

for i in ['Same Boro', 'Other Boro', 'Region']:
    fig = fig.add_trace(go.Bar(name = i,
                               x = dest.loc[dest['DEST'] == i, 'RES'],
                               y = dest.loc[dest['DEST'] == i, 'PWGTP'],
                               marker = {'color': dest_colors[i]},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = dest.loc[dest['DEST'] == i, 'HOVER']))
    
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Destination of Work by Borough of Residence for NYC Commuters<b>',
                           'font_size': 20,
                           'x': .5,
                           'xanchor': 'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'font_size': 16,
                            'x': .5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120},
                  xaxis = {'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'tickfont_size': 12,
                           'rangemode': 'nonnegative',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/dest.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
fig

fig.write_html(path + 'dest.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})

print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/dest.html')

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

tm = nyc_commuters[['RES','TM','PWGTP']].groupby(['RES', 'TM']).sum().reset_index()
tm_total = dest[['RES','PWGTP']].groupby(['RES']).sum().reset_index()
tm_total.columns = ['RES','TOTAL']
tm = pd.merge(tm,tm_total,how='inner',on='RES')
tm['% TM'] = tm['PWGTP']/tm['TOTAL']
tm.to_csv(path + 'tm.csv',index=False)

tm['HOVER']='<b>Residence: </b>'+tm['RES']+'<br><b>Travel Mode: </b>'+tm['TM']+'<br><b>Commuters: </b>'+tm['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm['% TM'].map('{:.0%}'.format)

tm_colors = {'Subway':'#729ece',
             'Rail':'#ff9e4a',
             'Bus':'#67bf5c',
             'Drive Alone': '#ed665d',
             'Carpool': '#ad8bc9',
             'Other': '#ed97ca',
             'Work From Home': '#6dccda'}

fig = go.Figure()

for i in ['Subway', 'Rail', 'Bus', 'Drive Alone', 'Carpool', 'Other', 'Work From Home']:
    fig = fig.add_trace(go.Bar(name = i,
                               x = tm.loc[tm['TM'] == i, 'RES'],
                               y = tm.loc[tm['TM'] == i, '% TM'],
                               marker = {'color': tm_colors[i]},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = tm.loc[tm['TM'] == i, 'HOVER']))
    
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Travel Mode to Work by Borough of Residence for NYC Commuters<b>',
                           'font_size': 20,
                           'x': .5,
                           'xanchor': 'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'font_size': 16,
                            'x': .5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120},
                  xaxis = {'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'tickfont_size': 12,
                           'tickformat': ',.0%',
                           'rangemode': 'nonnegative',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tm.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
fig

fig.write_html(path + 'tm.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})

print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/tm.html')

# determine mode split for commuters not living or working in manhattan
tm_not_mn = nyc_commuters[['RES', 'POW', 'TM', 'PWGTP']].groupby(['RES','POW','TM']).sum()
tm_not_mn = tm_not_mn.drop(index='Manhattan')
tm_not_mn = tm_not_mn.drop(index='Manhattan', level =1).reset_index()
tm_not_mn = tm_not_mn.groupby(['TM']).sum().reset_index()
tm_not_mn['% TM'] = tm_not_mn['PWGTP'] / tm_not_mn['PWGTP'].sum()

#sorter = ['Subway','Rail','Bus','Drive Alone','Carpool', 'Other', 'Work From Home']
#tm_not_mn = tm_not_mn.set_index('TM').loc[sorter].reset_index()

tm_not_mn.to_csv(path + 'tm_not_mn.csv',index=False)

tm_not_mn['HOVER']='<b>Travel Mode: </b>'+tm_not_mn['TM']+'<br><b>Commuters: </b>'+tm_not_mn['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm_not_mn['% TM'].map('{:.0%}'.format)


fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = tm_not_mn['TM'],  #need to add colors and arrange in order
                           values = tm_not_mn['% TM'],
                           hoverinfo = 'text',
                           hovertext = tm_not_mn['HOVER'])) 
    
fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Mode Split for Commuters Living or Working in the Outer Boroughs<b>',
                           'font_size': 20,
                           'x': .5,
                           'xanchor': 'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'font_size': 16,
                            'x': .5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tm_not_mn.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
fig

fig.write_html(path + 'tm_not_mn.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})

print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/tm_not_mn.html')

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


