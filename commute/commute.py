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
local_path = 'C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Projects/Conditions & Trends/Dec 2021/Input/'
#local_path = '/Users/Work/OneDrive - NYC O365 HOSTED/Projects/Conditions & Trends/Dec 2021/Input/'

# import ny, nj, ct, and pa pums files as one df
file_list = ['csv_pny.csv', 
             'csv_pct.csv', 
             'csv_pnj.csv', 
             'csv_ppa.csv']

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
pums_df['POWSP'] = pums_df['POWSP'].apply(lambda x: x.zfill(3))
pums_df['POWPUMA'] = pums_df['POWPUMA'].apply(lambda x: x.zfill(4))

# add columns with combined state and puma codes
pums_df['STPUMA'] = pums_df['ST'] + pums_df['PUMA']
pums_df['POWSPPUMA'] = pums_df['POWSP'] + pums_df['POWPUMA']
    
# create dictionary with puma codes for nyc, the region and their subgeos
codes_df = pd.read_excel(local_path + 'puma_codes.xlsx', dtype = str)
codes_df.to_dict(orient = 'list')

codes_dict = {}
for col in codes_df.columns: 
        codes_dict[col] = codes_df[col].dropna().to_list()

#%% WORKERS LIVING IN NYC

# create primary dataset for workers living in nyc
codes_dict['si']

nyc_commuters = pums_ny[pums_ny.PUMA.isin(nyc)]
nyc_commuters = pums_ny[pums_ny.PUMA.isin(nyc)]
nyc_commuters = nyc_commuters[nyc_commuters.POWPUMA.notna()]

# add plain text columns for residence & work locations and travel mode & time
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

test_df = nyc_commuters[['POWSP', 'PWGTP']].groupby(['POWSP']).sum()
test_df['PWGTP'].sum()

nyc_commuters['POWSPPUMA'] = nyc_commuters.POWSP.astype(str) + nyc_commuters.POWPUMA.astype(str)
nyc_commuters['POWSPPUMA'] = nyc_commuters.POWSPPUMA.astype(int)

nyc_commuters.dtypes
nyc_commuters['POW'] = np.select([(nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(bronx)), 
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(brooklyn)),
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(manhattan)), 
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(queens)),  
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(si)),
                                  nyc_commuters.POWSPPUMA.isin(region)],
                                  ['Bronx', 
                                  'Brooklyn', 
                                  'Manhattan', 
                                  'Queens', 
                                  'Staten Island',
                                  'Region'],
                                 default = 'Other')
                                 


nyc_commuters['POW'] = np.select([(nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(bronx)), 
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(brooklyn)),
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(manhattan)), 
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(queens)),  
                                  (nyc_commuters['POWSP'] == 36) & (nyc_commuters.POWPUMA.isin(si)),
                                  (nyc_commuters['POWSP'] == 36) & (~nyc_commuters.POWPUMA.isin(nyc)),
                                  nyc_commuters['POWSP'] == 34,
                                  nyc_commuters['POWSP'] == 9],
                                 ['Bronx', 
                                  'Brooklyn', 
                                  'Manhattan', 
                                  'Queens', 
                                  'Staten Island',
                                  'New York State',
                                  'New Jersey',
                                  'Connecticut'],
                                 default = 'Other')


    
nyc_commuters['DEST'] = np.select([nyc_commuters['POW'] == 'Region',
                                   nyc_commuters['RES'] == nyc_commuters['POW']],
                                  ['Region',
                                   'Same Boro'],
                                  default = 'Other Boro')

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
                                 nyc_commuters['JWMNP'] <= 60,
                                 nyc_commuters['JWMNP'] > 60],
                                ['nan',
                                 'Less Than 30 Mins', 
                                 '30 to 60 Mins',
                                 'More Than 60 Mins'])

# adjust annual income to constant dollars
nyc_commuters['INC'] = (nyc_commuters['ADJINC'] *.000001) * nyc_commuters['WAGP']

# determine income band based on ami
ami = 83600 #2021 nyc region 
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
                                              'POWPUMA',
                                              'JWRIP',
                                              'JWTRNS',
                                              'JWMNP',
                                              'ADJINC',
                                              'WAGP',
                                              'INC'])

# nyc_commuters.to_csv(path + 'nyc_commuters.csv', index = False)

#%% WORKERS LIVING OUTSIDE OF NYC

# create secondary dataset for workers living outside of nyc 
regional_commuters = pd.concat([pums_ny, pums_ct, pums_nj, pums_pa])
regional_commuters = regional_commuters[~regional_commuters.PUMA.isin(nyc)]
regional_commuters = regional_commuters[regional_commuters.POWPUMA.isin(nyc)]

# add plain text columns for residence & work locations 
regional_commuters['RES_STATE'] = np.select([regional_commuters['ST'] == 36,
                                             regional_commuters['ST'] == 34,
                                             regional_commuters['ST'] == 9,
                                             regional_commuters['ST'] == 42],
                                            ['New York',
                                             'New Jersey',
                                             'Connecticut',
                                             'Pennsylvania'])

# create dictionary with PUMAs for each regional geography 
reg_df = pd.read_csv(local_path + 'regional_pumas.csv')

li = reg_df['li'].dropna().to_list()
lhv = reg_df['lhv'].dropna().to_list()
mhv = reg_df['mhv'].dropna().to_list()
inj = reg_df['inj'].dropna().to_list()
onj = reg_df['onj'].dropna().to_list()
ct = reg_df['ct'].dropna().to_list()

regional_commuters['RES_REG'] = np.select([(regional_commuters['ST'] == 36) & (regional_commuters.PUMA.isin(li)),
                                           (regional_commuters['ST'] == 36) & (regional_commuters.PUMA.isin(lhv)),
                                           (regional_commuters['ST'] == 36) & (regional_commuters.PUMA.isin(mhv)),
                                           (regional_commuters['ST'] == 34) & (regional_commuters.PUMA.isin(inj)),
                                           (regional_commuters['ST'] == 34) & (regional_commuters.PUMA.isin(onj)),
                                           (regional_commuters['ST'] == 9) & (regional_commuters.PUMA.isin(ct))],
                                          ['Long Island',
                                           'Lower Hudson Valley',
                                           'Mid Hudson Valley',
                                           'Inner New Jersey',
                                           'Outer New Jersey',
                                           'Connecticut'],
                                          default = 'Other')                                          

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

# delete unused columns and save cleaned up dataset
regional_commuters = regional_commuters.drop(columns = ['SERIALNO', 
                                                        'ST', 
                                                        'PUMA', 
                                                        'POWPUMA',
                                                        'JWRIP',
                                                        'JWTRNS', 
                                                        'JWMNP', 
                                                        'ADJINC', 
                                                        'WAGP'])

# regional_commuters.to_csv(path + 'regional_commuters.csv', index = False)

#%% COMMUTING FLOWS

live_nyc = nyc_commuters['PWGTP'].sum()
live_work_nyc = nyc_commuters.loc[nyc_commuters['POW'] != 'Region']['PWGTP'].sum()
work_nyc = live_work_nyc + regional_commuters['PWGTP'].sum()

live_work_di = {'Type': ['Workers Living in NYC',
                         'Workers Working in NYC',
                         'Workers Living & Working in NYC', 
                         'Workers Living in NYC & Working Elsewhere', 
                         'Workers Living Elsewhere & Working in NYC'],
                'Workers': [live_nyc, 
                            work_nyc,
                            live_work_nyc, 
                            live_nyc - live_work_nyc, 
                            work_nyc - live_work_nyc]}

flows = pd.DataFrame(live_work_di)
# flows.to_csv(path + 'annotations/flows.csv', index = False)

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
                         text = [str('{:,}'.format(round(live_nyc - live_work_nyc, -2))) +'<br>Workers Living in NYC<br>& Working Elsewhere',
                                 str('{:,}'.format(round(live_work_nyc, -2))) + '<br>Workers Living<br>& Working in NYC',
                                 str('{:,}'.format(round(work_nyc - live_work_nyc, -2))) + '<br>Workers Living Elsewhere<br>& Working in NYC'],
                         mode = 'text',
                         textfont = {'size': 16,
                                     'family': 'Arial',
                                     'color': 'black'},
                         hoverinfo = 'none'))

fig.add_annotation(x = 0,
                   y = 2,
                   text = str('{:,}'.format(round(live_nyc, -2))) + '<br>Workers Living in NYC',
                   font = {'size': 16,
                           'family': 'Arial',
                           'color': '#729ece'},
                   showarrow = False)

fig.add_annotation(x = 3,
                   y = 0,
                   text = str('{:,}'.format(round(work_nyc, -2))) + '<br>Workers Working in NYC',
                   font = {'size': 16,
                           'family': 'Arial',
                           'color': '#ff9e4a'},
                   showarrow = False)

fig.update_xaxes(showticklabels = False, 
                 showgrid = False,
                 zeroline = False)

fig.update_yaxes(showticklabels = False, 
                  showgrid = False, 
                  zeroline = False)

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Commuting Flows<b>',
                            'font_size': 20,
                            'x': .5,
                            'xanchor': 'center',
                            'y': .95,
                            'yanchor': 'top'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/flows.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')

fig

# fig.write_html(path + 'annotations/flows.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/flows.html

#%% NYC COMMUTERS: DESTINATION

dest = nyc_commuters[['RES','DEST','PWGTP']].groupby(['RES', 'DEST']).sum().reset_index()
dest_total = dest[['RES', 'PWGTP']].groupby(['RES']).sum().reset_index()
dest_total.columns = ['RES', 'TOTAL']
dest = pd.merge(dest, dest_total, how = 'inner', on = 'RES')
dest['% DEST'] = dest['PWGTP'] / dest['TOTAL']

# dest.to_csv(path+'annotations/dest.csv',index=False)

path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/commute/'
dest=pd.read_csv(path+'annotations/dest.csv')
dest['HOVER']='<b>Residence: </b>'+dest['RES']+'<br><b>Workplace: </b>'+dest['DEST']+'<br><b>Commuters: </b>'+dest['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest['% DEST'].map('{:.0%}'.format)

dest_colors = {'Same Boro':'rgba(237,102,93,0.8)',
               'Other Boro':'rgba(114,158,206,0.8)',
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
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/dest.html')

#%% NYC COMMUTERS: TRAVEL MODE

tm = nyc_commuters[['RES','TM','PWGTP']].groupby(['RES', 'TM']).sum().reset_index()
tm_total = dest[['RES','PWGTP']].groupby(['RES']).sum().reset_index()
tm_total.columns = ['RES','TOTAL']
tm = pd.merge(tm, tm_total, how = 'inner', on = 'RES')
tm['% TM'] = tm['PWGTP'] / tm['TOTAL']

# tm.to_csv(path + 'annotations/tm.csv',index = False)

path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/commute/'
tm=pd.read_csv(path+'annotations/tm.csv')
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
                               x = tm.loc[tm['TM'] == mode, 'RES'],
                               y = tm.loc[tm['TM'] == mode, '% TM'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = tm.loc[tm['TM'] == mode, 'HOVER']))

    
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

fig.add_annotation(text = '*Other includes walked, taxi, bicycle, ferry, motorcycle and other',
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
#                 include_plotlyjs='cdn',
#                 config={'displayModeBar':False})

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

tm_not_mn['HOVER']='<b>Travel Mode: </b>'+tm_not_mn['TM']+'<br><b>Commuters: </b>'+tm_not_mn['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm_not_mn['% TM'].map('{:.0%}'.format)

fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = tm_not_mn['TM'],  
                           values = tm_not_mn['% TM'],
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
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
fig

# fig.write_html(path + 'annotations/tm_not_mn.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/tm_not_mn.html

#%% NYC COMMUTERS: TRAVEL TIME

tt = nyc_commuters[['RES', 'DEST', 'TT', 'PWGTP']].groupby(['RES', 'DEST', 'TT']).sum().reset_index()
tt_total = tt[['RES','DEST','PWGTP']].groupby(['RES','DEST']).sum().reset_index()
tt_total.columns = ['RES','DEST','TOTAL']
tt = pd.merge(tt, tt_total, how='inner', on=['RES','DEST'])
tt['% TT'] = tt['PWGTP']/ tt['TOTAL']

sorter = ['Same Boro', 'Other Boro', 'Region']
tt = tt.set_index('DEST').loc[sorter].reset_index()

# tt.to_csv(path + 'annotations/tt.csv', index = False)

# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/commute/'
# tt=pd.read_csv(path+'annotations/tt.csv')
tt['HOVER']='<b>Travel Time: </b>'+tt['TT']+'<br><b>Commuters: </b>'+tt['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tt['% TT'].map('{:.0%}'.format)

boro_li = ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
tt_li = ['Less Than 30 Mins','30 to 60 Mins','More Than 60 Mins']

tt_colors = {'Less Than 30 Mins':'rgba(109,204,218,0.8)',
             '30 to 60 Mins':'rgba(173,139,201,0.8)',
             'More Than 60 Mins':'rgba(237,102,93,0.8)'}

fig = ps.make_subplots(rows = 1,
                       cols = len(boro_li),
                       shared_yaxes = True,
                       subplot_titles = boro_li)

count = 0 

for boro in range(0, len(boro_li)):
    for time in range(0, len(tt_li)):
        fig = fig.add_trace(go.Bar(name = tt_li[time],
                                    x = tt.loc[(tt['RES'] == boro_li[boro]) & (tt['TT'] == tt_li[time]), 'DEST'],
                                    y = tt.loc[(tt['RES'] == boro_li[boro]) & (tt['TT'] == tt_li[time]), 'PWGTP'],
                                    marker = {'color': tt_colors[tt_li[time]]},
                                    hoverinfo = 'text',
                                    hovertext = tt.loc[(tt['RES'] == boro_li[boro]) & (tt['TT'] == tt_li[time]), 'HOVER'],
                                    legendgroup = tt_li[time],
                                    showlegend = True if count < 3 else False),
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

# fig.write_html(path+'annotations/tt.html',
#                 include_plotlyjs='cdn',
#                 config={'displayModeBar':False})

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
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/tt_mn.html

#%% NYC COMMUTERS: TRAVEL TIME (> 60 MINS)

tt_60 = nyc_commuters.loc[(nyc_commuters['TT'] == 'More Than 60 Mins') & (nyc_commuters['AMI'] != 'nan')]
tt_60 = tt_60[['DEST', 'AMI', 'TM', 'PWGTP']].groupby(['DEST', 'AMI', 'TM']).sum().reset_index()
tt_60_total = tt_60[['DEST','AMI', 'PWGTP']].groupby(['DEST','AMI']).sum().reset_index()
tt_60_total.columns = ['DEST','AMI','TOTAL']
tt_60 = pd.merge(tt_60, tt_60_total, how='inner', on=['DEST','AMI'])
tt_60['%'] = tt_60['PWGTP']/ tt_60['TOTAL']

sorter = ['Same Boro', 'Other Boro', 'Region']
tt_60 = tt_60.set_index('DEST').loc[sorter].reset_index()

# tt_60.to_csv(path + 'annotations/tt_60.csv', index = False)

tt_60['HOVER']='<b>Travel Mode: </b>'+tt_60['TM']+'<br><b>Commuters: </b>'+tt_60['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tt_60['%'].map('{:.0%}'.format)

ami_li = ['Extremely Low Income', 'Very Low Income', 'Low Income', 'Moderate Income','Middle Income', 'High Income']
tm_li = list(tm_colors.keys()) # defined in travel mode cell

fig = ps.make_subplots(rows = 1,
                       cols = len(ami_li),
                       shared_yaxes = True,
                       subplot_titles = ami_li)

count = 0 

for ami in range(0, len(ami_li)):
    for mode in range(0, len(tm_li)):
        fig = fig.add_trace(go.Bar(name = tm_li[mode],
                                    x = tt_60.loc[(tt_60['AMI'] == ami_li[ami]) & (tt_60['TM'] == tm_li[mode]), 'DEST'],
                                    y = tt_60.loc[(tt_60['AMI'] == ami_li[ami]) & (tt_60['TM'] == tm_li[mode]), 'PWGTP'],
                                    marker = {'color': tm_colors[tm_li[mode]]},
                                    hoverinfo = 'text',
                                    hovertext = tt_60.loc[(tt_60['AMI'] == ami_li[ami]) & (tt_60['TM'] == tm_li[mode]), 'HOVER'],
                                    legendgroup = tm_li[mode],
                                    showlegend = True if count < 7 else False),
                            row = 1,
                            col = ami + 1)        
        count = count + 1 
        
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Travel Mode by Income for NYC Commuters Traveling Over 60 Mins to Work </b>',
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
                            'r': 80,
                            't': 120},
                  xaxis = {'fixedrange': True, 
                           'showgrid': False},
                  yaxis = {'title': {'text': '<b>Number of Commuters</b>',
                                     'font_size': 14},
                            'tickfont_size': 12,
                            'rangemode': 'nonnegative',
                            'fixedrange': True,
                            'showgrid': True},
                  hoverlabel = {'font_size': 14},
                  font = {'family': 'Arial',
                          'color':'black'},
                  dragmode = False)
    
for ami in range(0, len(ami_li)):
    fig.layout.annotations[ami].update(y = -0.05,
                                       yanchor = 'top',
                                       text = '<b>' + ami_li[ami] + '</b>',
                                       font = {'size': 14,
                                               'family': 'Arial'})
    
fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tt_60.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')

fig

# fig.write_html(path + 'annotations/tt_60.html',
#                include_plotlyjs = 'cdn',
#                config = {'displayModeBar': False})

# https://nycplanning.github.io/td-trends/commute/annotations/tt_60.html

#%% REGIONAL IN-COMMUTERS (BY STATE): DESTINATION 

dest_rc_state = regional_commuters[['RES_STATE','POW', 'PWGTP']].groupby(['RES_STATE', 'POW']).sum().reset_index()
dest_rc_state_total = dest_rc_state[['RES_STATE', 'PWGTP']].groupby(['RES_STATE']).sum().reset_index()
dest_rc_state_total.columns = ['RES_STATE', 'TOTAL']
dest_rc_state = pd.merge(dest_rc_state, dest_rc_state_total, how = 'inner', on = ['RES_STATE'])
dest_rc_state['% DEST'] = dest_rc_state['PWGTP'] / dest_rc_state['TOTAL']

# dest_rc_state.to_csv(path + 'annotations/dest_rc_state.csv', index = False)

dest_rc_state['HOVER']='<b>Destination: </b>'+dest_rc_state['POW']+'<br><b>Commuters: </b>'+dest_rc_state['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest_rc_state['% DEST'].map('{:.0%}'.format)

boro_colors = {'Bronx': '#729ece',
               'Brooklyn': '#ff9e4a',
               'Manhattan': '#67bf5c',
               'Staten Island': '#ed665d',
               'Queens': '#ad8bc9'}

fig = go.Figure()

fig = ps.make_subplots(rows = 1, 
                       cols = 2,
                       shared_yaxes = True,
                       subplot_titles = ['New York', 'Non-New York'])
    
for boro, color in boro_colors.items():
    fig = fig.add_trace(go.Bar(name = boro,
                               x = dest_rc_state.loc[dest_rc_state['POW'] == boro, 'RES_STATE'],
                               y = dest_rc_state.loc[dest_rc_state['POW'] == boro, 'PWGTP'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = dest_rc_state.loc[dest_rc_state['POW'] == boro, 'HOVER']))

fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Destination of Work by State of Residence for Regional In-Commuters</b>',
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
                            'r': 80,
                            't': 120},
                  xaxis = {'title': {'text': '<b>State of Residence</b>',
                                     'font_size': 14},
                           'categoryorder': 'total descending',
                           'tickfont_size':14,
                           'fixedrange':True,
                           'showgrid':False},
                  yaxis = {'title': {'text': '<b>Number of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                          'rangemode': 'nonnegative',
                          'fixedrange': True,
                          'showgrid': True},
                  hoverlabel = {'font_size': 14},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode=False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/dest_rc_state.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')

fig   

# fig.write_html(path + 'annotations/dest_rc_state.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/dest_rc_state.html'

#%% REGIONAL IN-COMMUTERS (BY REGIONAL GEOGRAPHY): DESTINATION 

dest_rc_reg = regional_commuters[['RES_REG','POW', 'PWGTP']].groupby(['RES_REG', 'POW']).sum().reset_index()
dest_rc_reg = dest_rc_reg[dest_rc_reg.RES_REG != 'Other']
dest_rc_reg_total = dest_rc_reg[['RES_REG', 'PWGTP']].groupby(['RES_REG']).sum().reset_index()
dest_rc_reg_total.columns = ['RES_REG', 'TOTAL']
dest_rc_reg = pd.merge(dest_rc_reg, dest_rc_reg_total, how = 'inner', on = ['RES_REG'])
dest_rc_reg['% DEST'] = dest_rc_reg['PWGTP'] / dest_rc_reg['TOTAL']

# dest_rc_reg.to_csv(path + 'annotations/dest_rc_reg.csv', index = False)
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/commute/'
dest_rc_reg=pd.read_csv(path+'annotations/dest_rc_reg.csv')
dest_rc_reg['HOVER']='<b>Destination: </b>'+dest_rc_reg['POW']+'<br><b>Commuters: </b>'+dest_rc_reg['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest_rc_reg['% DEST'].map('{:.0%}'.format)

boro_colors = {'Bronx':'rgba(114,158,206,0.8)',
               'Brooklyn':'rgba(255,158,74,0.8)',
               'Manhattan':'rgba(103,191,92,0.8)',
               'Queens':'rgba(237,102,93,0.8)',
               'Staten Island':'rgba(173,139,201,0.8)'}

fig = go.Figure()
    
for boro, color in boro_colors.items():
    fig = fig.add_trace(go.Bar(name = boro,
                               x = dest_rc_reg.loc[dest_rc_reg['POW'] == boro, 'RES_REG'],
                               y = dest_rc_reg.loc[dest_rc_reg['POW'] == boro, 'PWGTP'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = dest_rc_reg.loc[dest_rc_reg['POW'] == boro, 'HOVER']))

fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Destination of Work by Place of Residence<br>for Regional In-Commuters</b>',
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
                  margin = {'b': 160,
                            'l': 80,
                            'r': 40,
                            't': 160},
                  xaxis = {'title': {'text': '<b>Place of Residence</b>',
                                     'font_size': 14},
                           'categoryorder': 'total descending',
                           'tickfont_size':14,
                           'fixedrange':True,
                           'showgrid':False},
                  yaxis = {'title': {'text': '<b>Number of Commuters</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                          'rangemode': 'nonnegative',
                          'fixedrange': True,
                          'showgrid': True},
                  hoverlabel = {'font_size': 14},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode=False)

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/dest_rc_reg.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y=0,
                   yanchor='top',
                   yref='paper',
                   yshift=-120)

fig   

# fig.write_html(path + 'annotations/dest_rc_reg.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/dest_rc_reg.html'
#%% REGIONAL IN-COMMUTERS: DESTINATION (ALL WORKERS LIVING IN NYC)
 
work_nyc_total = dest_rc_total.copy() # defined in destination cell
work_nyc_total = work_nyc_total.append({'RES': 'New York City', 'TOTAL': live_work_nyc}, ignore_index = True)
work_nyc_total.loc[2, 'RES'] = 'New York State'
work_nyc_total['% RES'] = work_nyc_total['TOTAL'] / work_nyc_total['TOTAL'].sum()
work_nyc_total = work_nyc_total.sort_values(by = 'TOTAL', ascending = False)

# work_nyc_total.to_csv(path + 'annotations/work_nyc_total.csv',index = False)

work_nyc_total['HOVER']='<b>Residence: </b>'+ work_nyc_total['RES']+'<br><b>Commuters: </b>'+ work_nyc_total['TOTAL'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+ work_nyc_total['% RES'].map('{:.0%}'.format)

work_nyc_colors = {'New York City':'#729ece',
                   'New York State':'#ff9e4a',
                   'Connecticut':'#67bf5c',
                   'New Jersey': '#ed665d',
                   'Pennsylvania': '#ad8bc9'}

fig = go.Figure()

for res, color in work_nyc_colors.items():    
 fig = fig.add_trace(go.Pie(labels = work_nyc_total['RES'],  
                            values = work_nyc_total['TOTAL'],
                            texttemplate = '%{percent:.0%}',
                            sort = True,
                            direction = 'clockwise',
                            marker = {'colors': list(work_nyc_colors.values())},
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
#               config={'displayModeBar':False})

# https://nycplanning.github.io/td-trends/commute/annotations/work_nyc_total.html')                            