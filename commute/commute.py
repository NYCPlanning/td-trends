# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Commuting 
Source: 2019 ACS 5-Year PUMS 
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import plotly.subplots as ps

pio.renderers.default = 'browser'
path = 'C:/Users/M_Free/Desktop/td-trends/commute/'
# path = '/Users/Work/Desktop/GitHub/td-trends/commute/'
# path = 'C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/commute/'
local_path = 'C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Projects/Conditions & Trends/Dec 2021/Input/'
#local_path = '/Users/Work/OneDrive - NYC O365 HOSTED/Projects/Conditions & Trends/Dec 2021/Input/'

# import ny, nj, ct, and pa pums files as one df
file_list = ['csv_pny.csv', 
             'csv_pct.csv', 
             'csv_pnj.csv']

col_list = ['SERIALNO', 
            'ST', 
            'PUMA', 
            'PWGTP',
            'POWSP',
            'POWPUMA',
            'JWRIP',
            'JWTRNS', 
            'JWMNP', 
            'ADJINC', 
            'WAGP']

pums_list = []
for file in file_list: 
    df = pd.read_csv(local_path + file, 
                     usecols = col_list, 
                     dtype = {'SERIALNO': str,
                              'ST': str, 
                              'PUMA': str,
                              'POWSP': str,
                              'POWPUMA': str})
    pums_list.append(df)

pums_df = pd.concat(pums_list, axis = 0, ignore_index = True)

# add leading zeros 
pums_df['ST'] = pums_df['ST'].apply(lambda x: x.zfill(3))
pums_df['PUMA'] = pums_df['PUMA'].apply(lambda x: x.zfill(4))
pums_df['POWSP'] = pums_df['POWSP'].apply(lambda x: x.zfill(3) if pd.isna(x) is False else x)
pums_df['POWPUMA'] = pums_df['POWPUMA'].apply(lambda x: x.zfill(4) if pd.isna(x) is False else x)

# add columns with combined state and puma codes
pums_df['STPUMA'] = pums_df['ST'] + pums_df['PUMA']
pums_df['POWSPPUMA'] = pums_df['POWSP'] + pums_df['POWPUMA']
    
# create dictionary with puma codes for nyc, the region and their subgeos
codes_df = pd.read_excel(local_path + 'puma_codes.xlsx', dtype = str)

codes_dict = {}
for col in codes_df.columns: 
        codes_dict[col] = codes_df[col].dropna().to_list()

#%% WORKERS LIVING IN NYC

# create primary dataset for workers who live in nyc and work in nyc or the region
nyc_commuters = pums_df[pums_df.STPUMA.isin(codes_dict['nyc'])]
nyc_commuters = nyc_commuters[(nyc_commuters.POWSPPUMA.isin(codes_dict['nyc'])) | 
                              (nyc_commuters.POWSPPUMA.isin(codes_dict['reg']))]

# add plain text columns for residence & work locations and travel mode & time
nyc_commuters['RES'] = np.select([nyc_commuters.STPUMA.isin(codes_dict['bx']),
                                  nyc_commuters.STPUMA.isin(codes_dict['bk']),
                                  nyc_commuters.STPUMA.isin(codes_dict['mn']),
                                  nyc_commuters.STPUMA.isin(codes_dict['qn']),
                                  nyc_commuters.STPUMA.isin(codes_dict['si'])],
                                 ['Bronx',
                                  'Brooklyn',
                                  'Manhattan',
                                  'Queens',
                                  'Staten Island'])

nyc_commuters['POW'] = np.select([nyc_commuters.POWSPPUMA.isin(codes_dict['bx']), 
                                  nyc_commuters.POWSPPUMA.isin(codes_dict['bk']),
                                  nyc_commuters.POWSPPUMA.isin(codes_dict['mn']), 
                                  nyc_commuters.POWSPPUMA.isin(codes_dict['qn']),  
                                  nyc_commuters.POWSPPUMA.isin(codes_dict['si']),
                                  nyc_commuters.POWSPPUMA.isin(codes_dict['reg'])],
                                 ['Bronx', 
                                  'Brooklyn', 
                                  'Manhattan', 
                                  'Queens', 
                                  'Staten Island',
                                  'Region'])
    
nyc_commuters['DEST'] = np.select([nyc_commuters['POW'] == 'Region',
                                   nyc_commuters['RES'] == nyc_commuters['POW']],
                                  ['Region',
                                   'Same Borough'],
                                  default = 'Different Borough')

tm_di = {2: 'Bus',
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

def get_tm(row):
    if np.isnan(row['JWRIP']) == True: 
        return tm_di[row['JWTRNS']]
    elif row['JWRIP'] == 1: 
        return 'Drive Alone'
    else: 
        return 'Carpool'
    
nyc_commuters['TM'] = nyc_commuters.apply(get_tm, axis=1)

nyc_commuters['TT'] = np.select([nyc_commuters['JWMNP'] == 'nan',
                                 nyc_commuters['JWMNP'] < 30,
                                 nyc_commuters['JWMNP'] < 60,
                                 nyc_commuters['JWMNP'] < 90,
                                 nyc_commuters['JWMNP'] >= 90],
                                ['nan',
                                 'Less than 30 Mins', 
                                 '30 to 59 Mins',
                                 '60 to 89 Mins',
                                 '90 Mins or More'])

# adjust annual income to constant dollars
nyc_commuters['INC'] = (nyc_commuters['ADJINC'] *.000001) * nyc_commuters['WAGP']

# determine income band based on ami
ami = 83600 #2021 ami for the nyc region for an indiviual 
nyc_commuters['AMI'] = np.select([nyc_commuters['INC'] == 0,
                                  nyc_commuters['INC'] <= (ami * .3),
                                  nyc_commuters['INC'] <= (ami * .5),
                                  nyc_commuters['INC'] <= (ami * .8),
                                  nyc_commuters['INC'] <= (ami * 1.2),
                                  nyc_commuters['INC'] <= (ami * 1.65),
                                  nyc_commuters['INC'] > (ami * 1.65)],
                                 ['nan',
                                  'Extremely Low Income',
                                  'Very Low Income',
                                  'Low Income',
                                  'Moderate Income',
                                  'Middle Income',
                                  'High Income'])

# delete unused columns and save cleaned up dataset
nyc_commuters = nyc_commuters.drop(columns = ['SERIALNO', 
                                              'ST',
                                              'PUMA',
                                              'POWSP',
                                              'POWPUMA',
                                              'JWRIP',
                                              'JWTRNS',
                                              'JWMNP',
                                              'ADJINC',
                                              'WAGP',
                                              'INC'])

# nyc_commuters.to_csv(path + 'nyc_commuters.csv', index = False)

#%% WORKERS LIVING IN THE REGION

# create secondary dataset for workers who live in the region and work in nyc 
reg_commuters = pums_df[pums_df.STPUMA.isin(codes_dict['reg'])]
reg_commuters = reg_commuters[reg_commuters.POWSPPUMA.isin(codes_dict['nyc'])]

# add plain text columns for residence & work locations and travel mode & time
reg_commuters['RES'] = np.select([reg_commuters.STPUMA.isin(codes_dict['li']),
                                  reg_commuters.STPUMA.isin(codes_dict['lhv']),
                                  reg_commuters.STPUMA.isin(codes_dict['mhv']),
                                  reg_commuters.STPUMA.isin(codes_dict['inj']),
                                  reg_commuters.STPUMA.isin(codes_dict['onj']),
                                  reg_commuters.STPUMA.isin(codes_dict['wct'])],
                                 ['Long Island',
                                  'Lower Hudson Valley',
                                  'Mid Hudson Valley',
                                  'Inner New Jersey',
                                  'Outer New Jersey',
                                  'Western Connecticut'])       

reg_commuters['POW'] = np.select([reg_commuters.POWSPPUMA.isin(codes_dict['bx']),
                                  reg_commuters.POWSPPUMA.isin(codes_dict['bk']),
                                  reg_commuters.POWSPPUMA.isin(codes_dict['mn']),
                                  reg_commuters.POWSPPUMA.isin(codes_dict['qn']),
                                  reg_commuters.POWSPPUMA.isin(codes_dict['si'])],
                                 ['Bronx',
                                  'Brooklyn',
                                  'Manhattan',
                                  'Queens',
                                  'Staten Island'])

reg_commuters['TM'] = reg_commuters.apply(get_tm, axis=1)

reg_commuters['TT'] = np.select([reg_commuters['JWMNP'] == 'nan',
                                 reg_commuters['JWMNP'] < 30,
                                 reg_commuters['JWMNP'] < 60,
                                 reg_commuters['JWMNP'] < 90,
                                 reg_commuters['JWMNP'] >= 90],
                                ['nan',
                                 'Less than 30 Mins', 
                                 '30 to 59 Mins',
                                 '60 to 89 Mins',
                                 '90 Mins or More'])

# delete unused columns and save cleaned up dataset
reg_commuters = reg_commuters.drop(columns = ['SERIALNO', 
                                              'ST', 
                                              'PUMA', 
                                              'POWSP',
                                              'POWPUMA',
                                              'JWRIP',
                                              'JWTRNS', 
                                              'JWMNP', 
                                              'ADJINC', 
                                              'WAGP'])

# reg_commuters.to_csv(path + 'reg_commuters.csv', index = False)

#%% METRO COMMUTERS: FLOWS 

live_nyc = nyc_commuters['PWGTP'].sum()
live_work_nyc = nyc_commuters.loc[nyc_commuters['POW'] != 'Region']['PWGTP'].sum()
work_nyc = live_work_nyc + reg_commuters['PWGTP'].sum()

live_work_di = {'Type': ['People Living in NYC', 
                         'People Working in NYC', 
                         'People Living & Working in NYC', 
                         'People Living in NYC & Working in the Region (Out-Commuters)', 
                         'People Living in the Region & Working in NYC (In-Commuters)'],
                'Workers': [live_nyc, 
                            work_nyc,
                            live_work_nyc, 
                            live_nyc - live_work_nyc, 
                            work_nyc - live_work_nyc]}

flows = pd.DataFrame(live_work_di)
# flows.to_csv(path + 'annotations/flows.csv', index = False)
flows = pd.read_csv(path + 'annotations/flows.csv')

fig = go.Figure()

fig.add_shape(type = 'circle', 
              line_color = '#729ece',
              fillcolor = '#729ece',
              opacity = .5,
              layer = 'below',
              x0 = 0, 
              y0 = 0, 
              x1 = 2,
              y1 = 2)

fig.add_shape(type = 'circle',
              line_color = '#ff9e4a',
              fillcolor = '#ff9e4a',
              opacity = .5,
              layer = 'below',
              x0 = 1, 
              y0 = 0, 
              x1 = 3,
              y1 = 2)

fig.add_trace(go.Scatter(x = [.5, 1.5, 2.5],
                         y = [1, 1, 1],
                         text = ['<b>'+str('{:,}'.format(round(list(flows.loc[flows['Type']=='People Living in NYC & Working Elsewhere in the Region (Out-Commuters)','Workers'])[0], -2))) +'</b><br>People Living<br>in NYC<br>& Working<br>Elsewhere in<br>the Region<br>(Out-Commuters)',
                                 '<b>'+str('{:,}'.format(round(list(flows.loc[flows['Type']=='People Living & Working in NYC','Workers'])[0], -2))) + '</b><br>People Living<br>& Working<br>in NYC',
                                 '<b>'+str('{:,}'.format(round(list(flows.loc[flows['Type']=='People Living Elsewhere in the Region & Working in NYC (In-Commuters)','Workers'])[0], -2))) + '</b><br>People Living<br>Elsewhere in<br>the Region<br>& Working<br>in NYC<br>(In-Commuters)'],
                         mode = 'text',
                         textfont = {'size': 16,
                                     'family': 'Arial',
                                     'color': 'black'},
                         hoverinfo = 'none'))

fig.add_annotation(x = 0,
                   y = 2,
                   text = '<b>'+str('{:,}'.format(round(list(flows.loc[flows['Type']=='People Living in NYC','Workers'])[0], -2))) + '</b><br>People Living<br>in NYC',
                   font = {'size': 16,
                           'family': 'Arial',
                           'color': '#729ece'},
                   showarrow = False)

fig.add_annotation(x = 3,
                   y = 0,
                   text = '<b>'+str('{:,}'.format(round(list(flows.loc[flows['Type']=='People Working in NYC','Workers'])[0], -2))) + '</b><br>People Working<br>in NYC',
                   font = {'size': 16,
                           'family': 'Arial',
                           'color': '#ff9e4a'},
                   showarrow = False)

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Commuting Flows for NYC Metro Region Workers</b>',
                            'font_size': 20,
                            'x': .5,
                            'xanchor': 'center',
                            'y': .95,
                            'yanchor': 'top'},
                  margin = {'b': 120, 
                            'l': 200,
                            'r': 200,
                            't': 120},
                  xaxis={'showticklabels':False,
                         'showgrid':False,
                         'zeroline':False},
                  yaxis={'showticklabels':False,
                         'showgrid':False,
                         'zeroline':False},                
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/flows.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x=1,
                   xanchor='right',
                   xref='paper',
                   y=0,
                   yanchor='top',
                   yref='paper',
                   yshift=-80)

fig

# fig.write_html(path + 'annotations/flows.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar': True,
#                       'displaylogo': False,
#                       'modeBarButtonsToRemove': ['zoom', 
#                                                   'pan', 
#                                                   'select', 
#                                                   'zoomIn', 
#                                                   'zoomOut', 
#                                                   'autoScale', 
#                                                   'resetScale', 
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/flows.html

#%% NYC COMMUTERS: DESTINATION

dest = nyc_commuters[['RES','DEST','PWGTP']].groupby(['RES', 'DEST']).sum().reset_index()
dest_total = dest[['RES', 'PWGTP']].groupby(['RES']).sum().reset_index()
dest_total.columns = ['RES', 'TOTAL']
dest = pd.merge(dest, dest_total, how = 'inner', on = 'RES')
dest['% DEST'] = dest['PWGTP'] / dest['TOTAL']

# dest.to_csv(path + 'annotations/dest.csv', index = False)
# dest = pd.read_csv(path + 'annotations/dest.csv')

dest['HOVER']='<b>Residence: </b>'+dest['RES']+'<br><b>Workplace: </b>'+dest['DEST']+'<br><b>Commuters: </b>'+dest['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest['% DEST'].map('{:.0%}'.format)

dest_colors = {'Same Borough':'rgba(237,102,93,0.8)',
               'Different Borough':'rgba(114,158,206,0.8)',
               'Region':'rgba(103,191,92,0.8)'}

fig = go.Figure()

for destination, color in dest_colors.items():
    fig = fig.add_trace(go.Bar(name = destination,
                               x = dest.loc[dest['DEST'] == destination, 'RES'],
                               y = dest.loc[dest['DEST'] == destination, 'PWGTP'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = dest.loc[dest['DEST'] == destination, 'HOVER']))
    
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
                            'r': 40,
                            't': 120},
                  xaxis = {'title': {'text': '<b>Borough of Residence</b>',
                                     'font_size': 14},
                           'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Number of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'rangemode': 'tozero',
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
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -80)
fig

# fig.write_html(path + 'annotations/dest.html',
#                 config = {'displayModeBar': True,
#                         'displaylogo': False,
#                         'modeBarButtonsToRemove': ['select',                                                   
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/dest.html')

#%% NYC COMMUTERS: TRAVEL MODE

tm = nyc_commuters[['RES','TM','PWGTP']].groupby(['RES', 'TM']).sum().reset_index()
tm_total = dest[['RES','PWGTP']].groupby(['RES']).sum().reset_index()
tm_total.columns = ['RES','TOTAL']
tm = pd.merge(tm, tm_total, how = 'inner', on = 'RES')
tm['% TM'] = tm['PWGTP'] / tm['TOTAL']

# tm.to_csv(path + 'annotations/tm.csv',index = False)
# tm = pd.read_csv(path + 'annotations/tm.csv')

tm['HOVER']='<b>Residence: </b>'+tm['RES']+'<br><b>Travel Mode: </b>'+tm['TM']+'<br><b>Commuters: </b>'+tm['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm['% TM'].map('{:.0%}'.format)

tm_colors = {'Drive Alone': 'rgba(237,102,93,0.8)',
             'Carpool': 'rgba(255,158,74,0.8)',
             'Subway': 'rgba(114,158,206,0.8)',
             'Rail': 'rgba(168,120,110,0.8)',
             'Bus': 'rgba(103,191,92,0.8)',
             'Other*': 'rgba(237,151,202,0.8)',
             'Work From Home': 'rgba(109,204,218,0.8)'}

fig = go.Figure()

for mode, color in tm_colors.items():
    fig = fig.add_trace(go.Bar(name = mode,
                               x = tm.loc[tm['TM'] == mode.replace('*',''), 'RES'],
                               y = tm.loc[tm['TM'] == mode.replace('*',''), '% TM'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = tm.loc[tm['TM'] == mode.replace('*',''), 'HOVER']))
    
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
                            'r': 40,
                            't': 120},
                  xaxis = {'title': {'text': '<b>Borough of Residence</b>',
                                     'font_size': 14},
                           'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Percent of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'tickformat': ',.0%',
                           'rangemode': 'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = '<i>*Other includes walked, taxi, bicycle, ferry, motorcycle and other',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -80)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tm.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -100)
fig

# fig.write_html(path + 'annotations/tm.html',
#                 include_plotlyjs = 'cdn',
#                 config = {'displayModeBar': True,
#                         'displaylogo': False,
#                         'modeBarButtonsToRemove': ['select',                                                   
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/tm.html

#%% NYC COMMUTERS: TRAVEL MODE (NOT MANHATTAN)

tm_not_mn = nyc_commuters[['RES', 'POW', 'TM', 'PWGTP']].groupby(['RES','POW','TM']).sum()
tm_not_mn = tm_not_mn.drop(index = 'Manhattan')
tm_not_mn = tm_not_mn.drop(index = 'Manhattan', level = 1).reset_index()
tm_not_mn = tm_not_mn.groupby(['TM']).sum().reset_index()
tm_not_mn['% TM'] = tm_not_mn['PWGTP'] / tm_not_mn['PWGTP'].sum()

sorter = ['Subway','Rail','Bus','Drive Alone','Carpool', 'Other', 'Work From Home']
tm_not_mn = tm_not_mn.set_index('TM').loc[sorter].reset_index()

# tm_not_mn.to_csv(path + 'annotations/tm_not_mn.csv', index = False)
# tm_not_mn = pd.read_csv(path + 'annotations/tm_not_mn.csv')

tm_not_mn['HOVER']='<b>Travel Mode: </b>'+tm_not_mn['TM']+'<br><b>Commuters: </b>'+tm_not_mn['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm_not_mn['% TM'].map('{:.0%}'.format)

fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = tm_not_mn['TM'],  
                           values = tm_not_mn['% TM'],
                           hole = .5,
                           texttemplate = '%{percent:.0%}',
                           sort = False,
                           direction = 'clockwise',
                           marker = {'colors': list(tm_colors.values())}, #defined in travel mode cell
                           hoverinfo = 'text',
                           hovertext = tm_not_mn['HOVER'])) 
    
fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Mode Split for Commuters Living or Working Outside of Manhattan<b>',
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
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -100)

fig.add_annotation(text = f'N = {tm_not_mn["PWGTP"].sum():,.0f}',
                   font_size = 14,
                   showarrow = False, 
                   x = .5,
                   y = .5)

fig.add_annotation(text = '<i>*Other includes walked, taxi, bicycle, ferry, motorcycle and other',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -80)
fig

# fig.write_html(path + 'annotations/tm_not_mn.html',
#               include_plotlyjs = 'cdn',
#               config = {'displayModeBar': True,
#                         'displaylogo': False})

# https://nycplanning.github.io/td-trends/commute/annotations/tm_not_mn.html

#%% NYC COMMUTERS: TRAVEL TIME

tt = nyc_commuters[['RES', 'DEST', 'TT', 'PWGTP']].groupby(['RES', 'DEST', 'TT']).sum().reset_index() 
tt = tt.loc[tt['TT'] != '0']
tt_total = tt[['RES','DEST','PWGTP']].groupby(['RES','DEST']).sum().reset_index()
tt_total.columns = ['RES','DEST','TOTAL']
tt = pd.merge(tt, tt_total, how='inner', on=['RES','DEST'])
tt['% TT'] = tt['PWGTP']/ tt['TOTAL']

sorter = ['Same Borough', 'Different Borough', 'Region']
tt = tt.set_index('DEST').loc[sorter].reset_index()

# tt.to_csv(path + 'annotations/tt.csv', index = False)
# tt = pd.read_csv(path + 'annotations/tt.csv')

tt['DEST_TITLE'] = tt['DEST']
tt['DEST_TITLE'] = tt['DEST_TITLE'].str.replace(' ', '<br>')


tt['HOVER']='<b>Travel Time: </b>'+tt['TT']+'<br><b>Commuters: </b>'+tt['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tt['% TT'].map('{:.0%}'.format)

boro_li = ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
tt_li = ['Less than 30 Mins','30 to 59 Mins', '60 to 89 Mins', '90 Mins or More']

tt_colors = {'Less than 30 Mins':'rgba(109,204,218,0.8)',
             '30 to 59 Mins':'rgba(173,139,201,0.8)',
             '60 to 89 Mins':'rgba(237,102,93,0.8)',
             '90 Mins or More': 'rgba(103,191,92,0.8)'}

fig = ps.make_subplots(rows = 1,
                       cols = len(boro_li),
                       shared_yaxes = True,
                       subplot_titles = boro_li)

count = 0 

for boro in range(0, len(boro_li)):
    for time in range(0, len(tt_li)):
        fig = fig.add_trace(go.Bar(name = tt_li[time],
                                    x = tt.loc[(tt['RES'] == boro_li[boro]) & (tt['TT'] == tt_li[time]), 'DEST_TITLE'],
                                    y = tt.loc[(tt['RES'] == boro_li[boro]) & (tt['TT'] == tt_li[time]), 'PWGTP'],
                                    marker = {'color': tt_colors[tt_li[time]]},
                                    hoverinfo = 'text',
                                    hovertext = tt.loc[(tt['RES'] == boro_li[boro]) & (tt['TT'] == tt_li[time]), 'HOVER'],
                                    legendgroup = tt_li[time],
                                    showlegend = True if count < 4 else False),
                            row = 1,
                            col = boro + 1)        
        count = count + 1 
        
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Travel Time to Work by Borough of Residence for NYC Commuters</b>',
                           'font_size': 20,
                           'x': 0.5,
                           'xanchor': 'center',
                           'y': 0.95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'title_text': '', 
                            'font_size': 16,
                            'x': 0.5, 
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120,
                            'l': 80,
                            'r': 40,
                            't': 120},
                  xaxis = {'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Number of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'rangemode': 'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14},
                  font = {'family': 'Arial',
                          'color':'black'},
                  dragmode = False)

for boro in range(0, len(boro_li)):
    fig.layout.annotations[boro].update(y = 0, 
                                        yanchor = 'top',
                                        yref = 'paper',
                                        yshift = -40,
                                        text = '<b>' + boro_li[boro] + '</b>',
                                        font = {'size': 14,
                                               'family': 'Arial'})
    
fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tt.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -80)

fig

# fig.write_html(path + 'annotations/tt.html',
#               include_plotlyjs = 'cdn',
#               config={'displayModeBar': True,
#                       'displaylogo': False,
#                       'modeBarButtonsToRemove': ['zoom', 
#                                                   'pan', 
#                                                   'select', 
#                                                   'zoomIn', 
#                                                   'zoomOut', 
#                                                   'autoScale', 
#                                                   'resetScale', 
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/tt.html

#%% NYC COMMUTERS: TRAVEL TIME (MANHATTAN vs. NOT MANHATTAN)

nyc_commuters['MN'] = np.select([nyc_commuters['POW'] == 'Manhattan'],
                                ['Manhattan Bound'], 
                                default='Non-Manhattan Bound')

tt_mn = nyc_commuters[['MN','TT', 'PWGTP']].groupby(['MN', 'TT']).sum().reset_index()
tt_mn_total = tt_mn[['MN', 'PWGTP']].groupby(['MN']).sum().reset_index()
tt_mn_total.columns = ['MN', 'TOTAL']
tt_mn = pd.merge(tt_mn, tt_mn_total, how = 'inner', on = ['MN'])
tt_mn['% TT'] = tt_mn['PWGTP'] / tt_mn['TOTAL']

# tt_mn.to_csv(path + 'annotations/tt_mn.csv', index = False)
# tt = pd.read_csv(path + 'annotations/tt_mn.csv')

tt_mn['HOVER']='<b>Travel Time: </b>'+tt_mn['TT']+'<br><b>Commuters: </b>'+tt_mn['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tt_mn['% TT'].map('{:.0%}'.format)

fig = go.Figure()

for time, color in tt_colors.items():
    fig = fig.add_trace(go.Bar(name = time,
                               x = tt_mn.loc[tt_mn['TT'] == time, 'MN'],
                               y = tt_mn.loc[tt_mn['TT'] == time, '% TT'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = tt_mn.loc[tt_mn['TT'] == time, 'HOVER']))

    
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Travel Time by Destination of Work for NYC Commuters<b>',
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
                  xaxis = {'title': {'text': '<b>Destination of Work</b>',
                                     'font_size': 14},
                           'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Percent of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'tickformat': ',.0%',
                           'rangemode': 'nonnegative',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tt_mn.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
fig

# fig.write_html(path + 'annotations/tt_mn.html',
#                 include_plotlyjs = 'cdn',
#                 config = {'displayModeBar': True,
#                         'displaylogo': False,
#                         'modeBarButtonsToRemove': ['select',                                                   
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/tt_mn.html

#%% NYC COMMUTERS: TRAVEL TIME (> 60 MINS)

tt_60 = nyc_commuters.loc[(nyc_commuters['TT'] == '60 to 89 Mins') | (nyc_commuters['TT'] == '90 Mins or More')]
tt_60 = tt_60.loc[nyc_commuters['AMI'] != 'nan']
tt_60 = tt_60[['AMI', 'DEST','PWGTP']].groupby(['AMI', 'DEST']).sum().reset_index()
tt_60_total = tt_60[['AMI','PWGTP']].groupby(['AMI']).sum().reset_index()
tt_60_total.columns = ['AMI','TOTAL']
tt_60 = pd.merge(tt_60, tt_60_total, how='inner', on=['AMI'])
tt_60['%'] = tt_60['PWGTP']/ tt_60['TOTAL']

sorter = ['Extremely Low Income', 'Very Low Income', 'Low Income', 'Moderate Income','Middle Income', 'High Income']
tt_60 = tt_60.set_index('AMI').loc[sorter].reset_index()

# tt_60.to_csv(path + 'annotations/tt_60.csv', index = False)
# tt_60 = pd.read_csv(path + 'annotations/tt_60.csv')

ami_dict = {'Extremely Low Income': '<br><i><=30% AMI', 
            'Very Low Income': '<br><i>31-50% AMI', 
            'Low Income': '<br><i>51-80% AMI', 
            'Moderate Income': '<br><i>81-120% AMI',
            'Middle Income': '<br><i>121-165% AMI', 
            'High Income': '<br><i>>165% AMI'}

tt_60['AMI_TITLE'] = tt_60['AMI'] + tt_60['AMI'].map(ami_dict)
tt_60['HOVER']='<b>Commuters: </b>'+tt_60['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tt_60['%'].map('{:.0%}'.format)

fig = go.Figure()

for destination, color in dest_colors.items():
    fig = fig.add_trace(go.Bar(name = destination,
                               x = tt_60.loc[tt_60['DEST'] == destination, 'AMI_TITLE'],
                               y = tt_60.loc[tt_60['DEST'] == destination, 'PWGTP'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = tt_60.loc[tt_60['DEST'] == destination, 'HOVER']))
    
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Income for NYC Commuters Traveling Over 60 Mins to Work<b>',
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
                            'r': 40,
                            't': 120},
                  xaxis = {'title': {'text': '<b>Income Band</b>',
                                     'font_size': 14},
                           'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Number of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'rangemode': 'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a>, <a href="https://www1.nyc.gov/site/hpd/services-and-information/area-median-income.page" target="blank">NYC HPD 2021 Individual AMI</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tt_60.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.125,
                   yanchor = 'top',
                   yref = 'paper')

fig

# fig.write_html(path + 'annotations/tt_60.html',
#                 config = {'displayModeBar': True,
#                         'displaylogo': False,
#                         'modeBarButtonsToRemove': ['select',                                                   
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/tt_60.html

#%% REGIONAL IN-COMMUTERS: DESTINATION 

dest_rc = reg_commuters[['RES','POW','PWGTP']].groupby(['RES','POW']).sum().reset_index()
dest_rc_total = dest_rc[['RES', 'PWGTP']].groupby(['RES']).sum().reset_index()
dest_rc_total.columns = ['RES', 'TOTAL']
dest_rc = pd.merge(dest_rc, dest_rc_total, how = 'inner', on = ['RES'])
dest_rc['% DEST'] = dest_rc['PWGTP'] / dest_rc['TOTAL']

# dest_rc.to_csv(path + 'annotations/dest_rc.csv', index = False)
# dest_rc = pd.read_csv(path + 'annotations/dest_rc.csv')

dest_rc['HOVER']='<b>Destination: </b>'+dest_rc['POW']+'<br><b>Commuters: </b>'+dest_rc['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest_rc['% DEST'].map('{:.0%}'.format)

boro_colors = {'Bronx':'rgba(114,158,206,0.8)',
               'Brooklyn':'rgba(255,158,74,0.8)',
               'Manhattan':'rgba(103,191,92,0.8)',
               'Queens':'rgba(237,102,93,0.8)',
               'Staten Island':'rgba(173,139,201,0.8)'}

fig = go.Figure()
    
for boro, color in boro_colors.items():
    fig = fig.add_trace(go.Bar(name = boro,
                               x = dest_rc.loc[dest_rc['POW'] == boro, 'RES'],
                               y = dest_rc.loc[dest_rc['POW'] == boro, 'PWGTP'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = dest_rc.loc[dest_rc['POW'] == boro, 'HOVER']))

fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Destination of Work for Regional In-Commuters</b>',
                           'font_size': 20,
                           'x': 0.5,
                           'xanchor': 'center',
                           'y': 0.95,
                           'yanchor': 'top'},
                  legend = {'traceorder': 'normal',
                            'orientation': 'h',
                            'title_text': '',
                            'font_size': 16,
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120,
                            'l': 80,
                            'r': 40,
                            't': 120},
                  xaxis = {'title': {'text': '<b>Subregion of Residence</b>',
                                     'font_size': 14},
                           'categoryorder': 'total descending',
                           'tickfont_size':14,
                           'fixedrange':True,
                           'showgrid':False},
                  yaxis = {'title': {'text': '<b>Number of In-Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                          'rangemode': 'nonnegative',
                          'fixedrange': True,
                          'showgrid': True},
                  hoverlabel = {'font_size': 14},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode=False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/dest_rc.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1 ,
                   yanchor='top',
                   yref='paper')

fig   

# fig.write_html(path + 'annotations/dest_rc.html',
#               include_plotlyjs='cdn',
#               config = {'displayModeBar': True,
#                         'displaylogo': False,
#                         'modeBarButtonsToRemove': ['select',                                                   
#                                                   'lasso2d']})

# https://nycplanning.github.io/td-trends/commute/annotations/dest_rc.html'

#%% REGIONAL IN-COMMUTERS: DESTINATION (ALL WORKERS LIVING IN NYC)
 
work_nyc_total = dest_rc_total.copy()
work_nyc_total = work_nyc_total.append({'RES': 'New York City', 'TOTAL': live_work_nyc}, ignore_index = True)
work_nyc_total['% RES'] = work_nyc_total['TOTAL'] / work_nyc_total['TOTAL'].sum()
work_nyc_total = work_nyc_total.sort_values(by = 'TOTAL', ascending = False)

# work_nyc_total.to_csv(path + 'annotations/work_nyc_total.csv',index = False)
# work_nyc_total = pd.read_csv(path + 'annotations/work_nyc_total.csv')

work_nyc_total['HOVER']='<b>Residence: </b>'+ work_nyc_total['RES']+'<br><b>Commuters: </b>'+ work_nyc_total['TOTAL'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+ work_nyc_total['% RES'].map('{:.0%}'.format)

work_nyc_colors = {'New York City':'rgba(237,102,93,0.8)',
                   'Long Island':'rgba(255,158,74,0.8)',
                   'Mid Hudson Valley': 'rgba(114,158,206,0.8)',
                   'Lower Hudson Valley': 'rgba(103,191,92,0.8)' ,
                   'Inner New Jersey':'rgba(237,151,202,0.8)',
                   'Outer New Jersey': 'rgba(109,204,218,0.8)',
                   'Western Connecticut': 'rgba(168,120,110,0.8)'}
    

fig = go.Figure()

for res, color in work_nyc_colors.items():    
 fig = fig.add_trace(go.Pie(labels = work_nyc_total['RES'],  
                            values = work_nyc_total['TOTAL'],
                            texttemplate = '%{percent:.0%}',
                            sort = True,
                            direction = 'clockwise',
                            marker = {'colors': list(work_nyc_colors.values())},
                            hole = .5,
                            hoverinfo = 'text',
                            hovertext = work_nyc_total['HOVER']))    
    
fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Place of Residence for NYC Workers<b>',
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

fig.add_annotation(text = f'N = {work_nyc_total["TOTAL"].sum():,.0f}',
                   font_size = 14,
                   showarrow = False, 
                   x = .5,
                   y = .5)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/work_nyc_total.csv" target="blank">Download Chart Data</a>',
                    font_size = 14,
                    showarrow = False, 
                    x = 1, 
                    xanchor = 'right',
                    xref = 'paper',
                    y = -.1,
                    yanchor = 'top',
                    yref = 'paper')
fig

# fig.write_html(path + 'annotations/work_nyc_total.html',
#               include_plotlyjs='cdn',
#               config = {'displayModeBar': True,
#                         'displaylogo': False})

# https://nycplanning.github.io/td-trends/commute/annotations/work_nyc_total.html')         

#%% REGIONAL IN-COMMUTERS: TRAVEL MODE (MANHATTAN vs. NOT MANHATTAN)                    

reg_commuters['MN'] = np.select([reg_commuters['POW'] == 'Manhattan'],
                                ['Manhattan Bound'], 
                                default='Non-Manhattan Bound')

tm_reg_not_mn = reg_commuters[['MN', 'TM', 'PWGTP']].groupby(['MN', 'TM']).sum()
tm_reg_not_mn_total = tm_reg_not_mn.groupby(['MN']).sum().reset_index()


tm_reg_not_mn_total.columns = ['MN', 'TOTAL']
tm_reg_not_mn = pd.merge(tm_reg_not_mn, tm_reg_not_mn_total, how = 'inner', on = ['MN']) #losing tm column here, fix
tm_reg_not_mn['% TM'] = tm_reg_not_mn['PWGTP'] / tm_reg_not_mn['TOTAL']

sorter = ['Subway','Rail','Bus','Drive Alone','Carpool', 'Other', 'Work From Home']
tm_reg_not_mn = tm_reg_not_mn.set_index('TM').loc[sorter].reset_index()

# tm_reg_not_mn.to_csv(path + 'annotations/tm_reg_not_mn.csv', index = False)
# tm_reg_not_mn = pd.read_csv(path + 'annotations/tm_reg_not_mn.csv')

tm_reg_not_mn['HOVER']='<b>Travel Mode: </b>' + tm_reg_not_mn['TM'] + '<br><b>Commuters: </b>' + tm_reg_not_mn['PWGTP'].map('{:,.0f}'.format) + '<br><b>Percentage: </b>' + tm_reg_not_mn['% TM'].map('{:.0%}'.format)

fig = go.Figure()

for mode, color in tm_colors.items():
    fig = fig.add_trace(go.Bar(name = mode,
                               x = tm_reg_not_mn.loc[tm_reg_not_mn['TM'] == mode, 'MN'],
                               y = tm_reg_not_mn.loc[tm_reg_not_mn['TM'] == mode, '% TM'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = tm_reg_not_mn.loc[tm_reg_not_mn['TM'] == mode, 'HOVER']))
    
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Travel Mode to Work for Regional In-Commuters<b>',
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
                            'r': 40,
                            't': 120},
                  xaxis = {'title': {'text': '<b>Destination of Work</b>',
                                     'font_size': 14},
                           'tickfont_size': 14,
                           'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Percent of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'tickformat': ',.0%',
                           'rangemode': 'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = '<i>*Other includes walked, taxi, bicycle, ferry, motorcycle and other',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -80)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tm_reg_not_mn.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = 0,
                   yanchor = 'top',
                   yref = 'paper',
                   yshift = -100)
fig

# fig.write_html(path + 'annotations/tm_reg_not_mn.html',
#                include_plotlyjs = 'cdn',
#                config = {'displayModeBar': True,
#                         'displaylogo': False,
#                         'modeBarButtonsToRemove': ['select',                                                   
#                                                   'lasso2d']})
# https://nycplanning.github.io/td-trends/commute/annotations/tm_reg_not_mn.html

#%% REGIONAL IN-COMMUTERS: TRAVEL TIME  