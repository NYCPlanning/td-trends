# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Commuting 

Source: 2019 ACS 5-Year PUMS
Date: November - December 2021 
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import plotly.subplots as ps

pio.renderers.default = 'browser'

path = 'C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/'
#path = '/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/'

col_list = ['SERIALNO', 'ST', 'PUMA', 'PWGTP', 'POWPUMA','JWRIP','JWTRNS', 'JWMNP']

pums_ny = pd.read_csv(path + 'csv_pny.csv', usecols=col_list, dtype={'SERIALNO': str})
pums_ct = pd.read_csv(path + 'csv_pct.csv', usecols=col_list, dtype={'SERIALNO': str})
pums_nj= pd.read_csv(path + 'csv_pnj.csv', usecols=col_list, dtype={'SERIALNO': str})
pums_pa = pd.read_csv(path + 'csv_ppa.csv', usecols=col_list, dtype={'SERIALNO': str})

# assign puma codes for each boro 
bronx = list(range(3700,3711))
brooklyn = list(range(4000,4019))
manhattan = list(range(3800,3811))
queens = list(range(4100,4115))
si = list(range(3900,3904))
nyc = bronx + brooklyn + manhattan + queens + si

#%% COMMUTING FLOWS

nyc_commuters = pums_ny[pums_ny.PUMA.isin(nyc)]
nyc_commuters = nyc_commuters[nyc_commuters.POWPUMA.notna()] # github csv

regional_commuters = pd.concat([pums_ny, pums_ct, pums_nj, pums_pa])
regional_commuters = regional_commuters[~regional_commuters.PUMA.isin(nyc)]
regional_commuters = regional_commuters[regional_commuters.POWPUMA.isin(nyc)]  

live_nyc = nyc_commuters['PWGTP'].sum()
live_work_nyc = nyc_commuters[nyc_commuters.POWPUMA.isin(nyc)]['PWGTP'].sum()
work_nyc = live_work_nyc + regional_commuters['PWGTP'].sum()

data = {'Type': ['Workers Living in NYC',
                 'Workers Working in NYC',
                 'Workers Living & Working in NYC', 
                 'Workers Living in NYC & Working Elsewhere', 
                 'Workers Living Elsewhere & Working in NYC'],
        'Workers': [live_nyc, 
                    work_nyc,
                    live_work_nyc, 
                    live_nyc - live_work_nyc, 
                    work_nyc - live_work_nyc]}

flows = pd.DataFrame(data)
# flows.to_csv(path + 'flows.csv', index = False)

fig = go.Figure()

# create venn diagram 
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
                         text = [str('{:,}'.format(live_nyc - live_work_nyc)) +'<br>Workers Living in NYC<br>& Working Elsewhere',
                                 str('{:,}'.format(live_work_nyc)) + '<br>Workers Living<br>& Working in NYC',
                                 str('{:,}'.format(work_nyc - live_work_nyc)) + '<br>Workers Living Elsewhere<br>& Working in NYC'],
                         mode = 'text',
                         textfont = {'size': 16,
                                     'family': 'Arial',
                                     'color': 'black'},
                         hoverinfo = 'none'))

fig.add_annotation(x = 0,
                   y = 2,
                   text = str('{:,}'.format(live_nyc)) + '<br>Workers Living in NYC',
                   font = {'size': 16,
                           'family': 'Arial',
                           'color': '#729ece'},
                   showarrow = False)

fig.add_annotation(x = 3,
                   y = 0,
                   text = str('{:,}'.format(work_nyc)) + '<br>Workers Working in NYC',
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

# fig

# fig.write_html(path + 'flows.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/flows.html')

#%% NYC COMMUTERS: DESTINATION

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
dest_total = dest[['RES', 'PWGTP']].groupby(['RES']).sum().reset_index()
dest_total.columns = ['RES', 'TOTAL']
dest = pd.merge(dest, dest_total, how = 'inner', on = 'RES')
dest['% DEST'] = dest['PWGTP'] / dest['TOTAL']

# dest.to_csv(path+'dest.csv',index=False)

dest['HOVER']='<b>Residence: </b>'+dest['RES']+'<br><b>Workplace: </b>'+dest['DEST']+'<br><b>Commuters: </b>'+dest['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest['% DEST'].map('{:.0%}'.format)

dest_colors = {'Same Boro':'#729ece',
               'Other Boro':'#ff9e4a',
               'Region':'#67bf5c'}

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
#fig

#fig.write_html(path + 'dest.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

#print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/dest.html')

#%% NYC COMMUTERS: TRAVEL MODE

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

#tm.to_csv(path + 'tm.csv',index=False)

tm['HOVER']='<b>Residence: </b>'+tm['RES']+'<br><b>Travel Mode: </b>'+tm['TM']+'<br><b>Commuters: </b>'+tm['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm['% TM'].map('{:.0%}'.format)

tm_colors = {'Subway':'#729ece',
             'Rail':'#ff9e4a',
             'Bus':'#67bf5c',
             'Drive Alone': '#ed665d',
             'Carpool': '#ad8bc9',
             'Other': '#ed97ca',
             'Work From Home': '#6dccda'}

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
#fig

#fig.write_html(path + 'tm.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

#print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/tm.html')

# determine mode split for commuters not living or working in manhattan
tm_not_mn = nyc_commuters[['RES', 'POW', 'TM', 'PWGTP']].groupby(['RES','POW','TM']).sum()
tm_not_mn = tm_not_mn.drop(index='Manhattan')
tm_not_mn = tm_not_mn.drop(index='Manhattan', level =1).reset_index()
tm_not_mn = tm_not_mn.groupby(['TM']).sum().reset_index()
tm_not_mn['% TM'] = tm_not_mn['PWGTP'] / tm_not_mn['PWGTP'].sum()

sorter = ['Subway','Rail','Bus','Drive Alone','Carpool', 'Other', 'Work From Home']
tm_not_mn = tm_not_mn.set_index('TM').loc[sorter].reset_index()

#tm_not_mn.to_csv(path + 'tm_not_mn.csv',index=False)

tm_not_mn['HOVER']='<b>Travel Mode: </b>'+tm_not_mn['TM']+'<br><b>Commuters: </b>'+tm_not_mn['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tm_not_mn['% TM'].map('{:.0%}'.format)


fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = tm_not_mn['TM'],  
                           values = tm_not_mn['% TM'],
                           sort = False,
                           direction = 'clockwise',
                           marker = {'colors': list(tm_colors.values())},
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
#fig

# fig.write_html(path + 'tm_not_mn.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

#print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/tm_not_mn.html')

#%% NYC COMMUTERS: TRAVEL TIME

nyc_commuters['MN'] = np.select([nyc_commuters['POW'] == 'Manhattan'],
                                ['Manhattan Bound'], 
                                default='Non-Manhattan Bound')

nyc_commuters['TT'] = np.select([nyc_commuters['JWMNP'] < 30, 
                                 nyc_commuters['JWMNP'] < 60],
                                ['Less Than 30 Mins', 
                                 '30 to 60 Mins'],
                                default='More Than 60 Mins')

tt = nyc_commuters[['RES', 'DEST', 'TT', 'PWGTP']].groupby(['RES', 'DEST', 'TT']).sum().reset_index()

tt_total=tt[['RES','DEST','PWGTP']].groupby(['RES','DEST']).sum().reset_index()
tt_total.columns=['RES','DEST','TOTAL']
tt = pd.merge(tt,tt_total,how='inner',on=['RES','DEST'])
tt['% TT'] = tt['PWGTP']/ tt['TOTAL']

sorter = ['Same Boro', 'Other Boro', 'Region']
tt = tt.set_index('DEST').loc[sorter].reset_index()

#tt.to_csv(path + 'tt.csv', index = False)

tt['HOVER']='<b>Travel Time: </b>'+tt['TT']+'<br><b>Commuters: </b>'+tt['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+tt['% TT'].map('{:.0%}'.format)

boros = ['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
tt_cat = ['Less Than 30 Mins','30 to 60 Mins','More Than 60 Mins']

tt_colors = {'Less Than 30 Mins':'#729ece',
             '30 to 60 Mins':'#ff9e4a',
             'More Than 60 Mins':'#67bf5c'}

fig = ps.make_subplots(rows = 1,
                       cols = len(boros),
                       shared_yaxes = True,
                       subplot_titles = boros)

count = 0 

for boro in range(0, len(boros)):
    for cat in range(0, len(tt_cat)):
        fig = fig.add_trace(go.Bar(name = tt_cat[cat],
                                    x = tt.loc[(tt['RES'] == boros[boro]) & (tt['TT'] == tt_cat[cat]), 'DEST'],
                                    y = tt.loc[(tt['RES'] == boros[boro]) & (tt['TT'] == tt_cat[cat]), 'PWGTP'],
                                    marker = {'color': tt_colors[tt_cat[cat]]},
                                    hoverinfo = 'text',
                                    hovertext = tt.loc[(tt['RES'] == boros[boro]) & (tt['TT'] == tt_cat[cat]), 'HOVER'],
                                    legendgroup = tt_cat[cat],
                                    showlegend = True if count < 3 else False),
                            row = 1,
                            col = boro + 1)        
        count = count + 1 
        
fig.update_layout(barmode = 'stack',
                  template = 'plotly_white',
                  title = {'text': '<b>Travel Time to Destination of Work by Borough of Residence for NYC Commuters</b>',
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
                  yaxis = {'tickfont_size': 12,
                           'rangemode': 'nonnegative',
                           'fixedrange': True,
                           'showgrid': True},
                  hoverlabel = {'font_size': 14},
                  font = {'family': 'Arial',
                          'color':'black'},
                  dragmode = False)
    
for boro in range(0, len(boros)):
    fig.layout.annotations[boro].update(y = -0.05, yanchor = 'top')
    
fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tt.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')

#fig

# fig.write_html(path+'tt.html',
#                 include_plotlyjs='cdn',
#                 config={'displayModeBar':False})

#print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/tt.html')

# determine travel time by manhattan or non-manhattan destinations
tt_mn = nyc_commuters[['MN','TT', 'PWGTP']].groupby(['MN', 'TT']).sum().reset_index()

tt_mn_total = tt_mn[['MN', 'PWGTP']].groupby(['MN']).sum().reset_index()
tt_mn_total.columns = ['MN', 'TOTAL']
tt_mn = pd.merge(tt_mn, tt_mn_total, how = 'inner', on = ['MN'])
tt_mn['% TT'] = tt_mn['PWGTP'] / tt_mn['TOTAL']

#tt_mn.to_csv(path + 'tt_mn.csv', index = False)

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

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/tt_mn.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')
# fig

# fig.write_html(path + 'tt_mn.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/tt_mn.html')

#%% REGIONAL IN-COMMUTERS: DESTINATION

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

dest_rc_total = dest_rc[['RES', 'PWGTP']].groupby(['RES']).sum().reset_index()
dest_rc_total.columns = ['RES', 'TOTAL']
dest_rc = pd.merge(dest_rc, dest_rc_total, how = 'inner', on = ['RES'])
dest_rc['% DEST'] = dest_rc['PWGTP'] / dest_rc['TOTAL']

#dest_rc.to_csv(path + 'dest_rc.csv', index = False)

dest_rc['HOVER']='<b>Destination: </b>'+dest_rc['POW']+'<br><b>Commuters: </b>'+dest_rc['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest_rc['% DEST'].map('{:.0%}'.format)

boro_colors = {'Bronx': '#729ece',
               'Brooklyn': '#ff9e4a',
               'Manhattan': '#67bf5c',
               'Staten Island': '#ed665d',
               'Queens': '#ad8bc9'}

fig = go.Figure()
    
for boro, color in boro_colors.items():
    fig = fig.add_trace(go.Bar(name = boro,
                               x = '<b>'+ dest_rc.loc[dest_rc['POW'] == boro, 'RES']+'<b>',
                               y = dest_rc.loc[dest_rc['POW'] == boro, 'PWGTP'],
                               marker = {'color': color},
                               width = .5,
                               hoverinfo = 'text',
                               hovertext = dest_rc.loc[dest_rc['POW'] == boro, 'HOVER']))

fig.update_layout(
    barmode='stack',
    template='plotly_white',
    title={'text':'<b>Destination of Work by State of Residence for Regional In-Commuters</b>',
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

fig.add_annotation(text = 'Data Source: <a href="https://www.census.gov/programs-surveys/acs/microdata/access.2019.html" target="blank">Census Bureau 2019 ACS 5-Year PUMS</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/commute/annotations/dest_rc.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y = -.1,
                   yanchor = 'top',
                   yref = 'paper')

# fig   

# fig.write_html(path + 'dest_rc.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/dest_rc.html')    

# determine residence for all people working in nyc
 
work_nyc_total = dest_rc_total.copy()
work_nyc_total = work_nyc_total.append({'RES': 'New York City', 'TOTAL': live_work_nyc}, ignore_index = True)
work_nyc_total.loc[2, 'RES'] = 'New York State'
work_nyc_total['% RES'] = work_nyc_total['TOTAL'] / work_nyc_total['TOTAL'].sum()
work_nyc_total = work_nyc_total.sort_values(by = 'TOTAL', ascending = False)

# work_nyc_total.to_csv(path + 'work_nyc_total.csv',index = False)

work_nyc_total['HOVER']='<b>Residence: </b>'+ work_nyc_total['RES']+'<br><b>Commuters: </b>'+ work_nyc_total['TOTAL'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+ work_nyc_total['% RES'].map('{:.0%}'.format)

work_nyc_colors = {'New York City':'#729ece',
                   'New York State':'#ff9e4a',
                   'Connecticut':'#67bf5c',
                   'New Jersey': '#ed665d',
                   'Pennsylvanial': '#ad8bc9'}

fig = go.Figure()

for res, color in work_nyc_colors.items():    
 fig = fig.add_trace(go.Pie(labels = work_nyc_total['RES'],  
                            values = work_nyc_total['TOTAL'],
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
# fig

# fig.write_html(path + 'work_nyc_total.html',
#               include_plotlyjs='cdn',
#               config={'displayModeBar':False})

# print('Chart Available at: https://nycplanning.github.io/td-trends/commute/annotations/work_nyc_total.html')                                    