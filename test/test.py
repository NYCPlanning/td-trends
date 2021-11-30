import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

pio.renderers.default = 'browser'
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/test/'

# assign puma codes for each boro 
bronx = list(range(3700,3711))
brooklyn = list(range(4000,4019))
manhattan = list(range(3800,3811))
queens = list(range(4100,4115))
si = list(range(3900,3904))
nyc = bronx + brooklyn + manhattan + queens + si



# NYC COMMUTERS: DESTINATION
nyc_commuters=pd.read_csv(path+'nyc_commuters.csv',dtype=float,converters={'SERIALNO':str})

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

nyc_commuters['DEST'] = np.select([nyc_commuters.POW=='Region', 
                                  nyc_commuters.RES==nyc_commuters.POW],
                                 ['Region', 
                                  'Same Boro'],
                                 default='Other Boro')

dest = nyc_commuters[['RES','DEST','PWGTP']].groupby(['RES', 'DEST']).sum().reset_index()


fig=go.Figure()
for i in ['Same Boro','Other Boro','Region']:
    fig=fig.add_trace(go.Bar(x=dest.loc[dest['DEST']==i,'RES'],
                             y=dest.loc[dest['DEST']==i,'PWGTP']))
fig=fig.update_layout(barmode='stack')    
fig

dest_fig = px.bar(dest, 
                  x = 'RES', 
                  y = 'PWGTP', 
                  color = 'DEST',
                  labels = {'RES':'Residence', 
                            'PWGTP':'Number of Workers', 
                            'DEST':'Destination'},
                  category_orders= {'DEST': ['Same Boro','Other Boro','Region']},
                  title = 'Destination of Work by Borough of Residence for NYC Commuters')
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
nyc_commuters

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
                category_orders={'TM':['Subway', 'Rail', 'Bus','Drive Alone', 'Carpool', 'Other', 'Work From Home']},
                title = '<b>Travel Mode to Work by Borough of Residence for NYC Commuters<b>')
tm_fig.update_layout(yaxis_tickformat = '.1%')
tm_fig.show()

# determine mode split for commuters not living or working in manhattan
tm_not_mn = ~nyc_commuters[['RES', 'POW', 'TM', 'PWGTP']].isin('Manhattan')
tm_not_mn


tm_not_mn = tm_not_mn.groupby(['TM']).sum() 

# NYC COMMUTERS: TRAVEL TIME

nyc_commuters['MN'] = np.select([nyc_commuters['POW'] == 'Manhattan'],
                                ['Manhattan Bound'], 
                                default='Non-Manhattan Bound')

nyc_commuters['TT'] = np.select([nyc_commuters['JWMNP'] < 30, nyc_commuters['JWMNP'] < 60],
                                ['Less Than 30 Mins', '30 to 60 Mins'],
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
                category_orders={'TT': ['Less Than 30 Mins','30 to 60 Mins', 'More Than 60 Mins'], 
                                 'DEST':['Same Boro','Other Boro','Region']},
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
                   category_orders={'TT': ['Less Than 30 Mins','30 to 60 Mins', 'More Than 60 Mins']},
                   title = 'Travel Time by Place of Work for NYC Commuters')
tt_mn_fig.update_layout(yaxis_tickformat = '.1%')
tt_mn_fig.show()

nyc_commuters.to_csv()

