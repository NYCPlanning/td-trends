# -*- coding: utf-8 -*-
"""
Travel Conditions and Trends Update for Biking

Source(s): NYC DOHMH Community Health Survey 2020, NYC DOT Bicycle Counts, Citi Bike Operating Reports
Date: December 2021 - January 2022 
"""
import pyreadstat
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import datetime
import numpy as np

pio.renderers.default = 'browser'

path = 'C:/Users/M_Free/Desktop/td-trends/bike/annotations/'
# path = '/Users/Work/Desktop/GitHub/td-trends/bike/annotations/'
local_path = 'C:/Users/M_Free/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/'
# local_path = '/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/' 

#%% CYCLISTS

cols = ['cyclingfreq', 'wt21_dual']
chs, meta = pyreadstat.read_sas7bdat(local_path + 'chs2020_public.sas7bdat', usecols=cols)

chs = chs.groupby(['cyclingfreq']).sum().reset_index()

# combine never and unable to bike 
var = chs['wt21_dual'][4] + chs['wt21_dual'][5]
chs = chs.append({'cyclingfreq': 7, 'wt21_dual': var}, ignore_index = True)
chs = chs.drop(labels = [4,5], axis = 0)

chs['%'] = chs['wt21_dual'] / chs['wt21_dual'].sum()

chs = chs.replace({1:'Once a Week or More',
                   2:'Several Times a Month',
                   3:'At Least Once a Month',
                   4:'A Few Times a Year',
                   7:'Never or Unable'})

# chs.to_csv(path + 'chs.csv',index=False)
path = 'C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/bike/annotations/'
chs=pd.read_csv(path+'chs.csv')
chs['hover'] = '<b>Frequency: </b>'+ chs['cyclingfreq'] + '<br><b>Adults: </b>' + chs['wt21_dual'].map('{:,.0f}'.format) +'<br><b>Percentage: </b>' + chs['%'].map('{:.0%}'.format)

chs_colors = {'Once a Week or More': 'rgba(237,102,93,0.8)',
              'Several Times a Month': 'rgba(255,158,74,0.8)',
              'At Least Once a Month': 'rgba(173,139,201,0.8)',
              'A Few Times a Year': 'rgba(114,158,206,0.8)',
              'Never or Unable': 'rgba(162,162,162,0.8)'}

fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = chs['cyclingfreq'],
                           values = chs['%'],
                           hole = .5,
                           sort = False,
                           direction = 'clockwise',
                           pull=0.05,
                           marker = {'colors': list(chs_colors.values())},
                           textinfo = 'text',
                           text= chs['%'].map('{:.0%}'.format),
                           textfont={'size':14},
                           hoverinfo = 'text',
                           hovertext = chs['hover']))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Adult New Yorkers Who Ride a Bike<b>',
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
                  margin = {'b': 40, 
                            'l': 80,
                            'r': 80,
                            't': 200},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www1.nyc.gov/site/doh/data/data-sets/community-health-survey-public-use-data.page" target="blank">NYC DOHMH 2020</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/annotations/chs.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y=0,
                   yanchor='top',
                   yref='paper',
                   yshift=0)
fig.add_annotation(text = f'N = {chs["wt21_dual"].sum():,.0f}',
                   font_size = 14,
                   showarrow = False, 
                   x = .5,
                   y = .5)
                  
fig 

# fig.write_html(path + 'chs.html', include_plotlyjs='cdn', config={'displayModeBar':False})
# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/chs.html')

#%% BIKE COUNTS

parser = lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p') # 8/31/2012  12:00:00 AM                 
counts = pd.read_csv(local_path + 'bicycle_counts.csv', parse_dates = ['date'], date_parser = parser)

counters = pd.read_csv(local_path + 'bicycle_counters.csv', usecols = ['name', 'site', 'latitude','longitude'])

# active counters
counter_list = [100009425, 100009427, 100009428, 100010017, 100010018, 100010019, 100062893, 300020904]

counts = counts[counts.site.isin(counter_list)]
counts = counts.groupby(['site', pd.Grouper(key = 'date', freq = 'M')])['counts'].sum().reset_index()
# time = counts.groupby(['site']).agg({'date': ['min','max'], 'counts':'sum'})
counts = counts[counts['date'] > '2017-05-31']

counts = pd.merge(counts, counters[['name', 'site']], how = 'inner', on = 'site')
counts['name'] = counts['name'].replace({'Ed Koch Queensboro Bridge Shared Path': 'Queensboro Bridge',
                                         'Kent Ave btw North 8th St and North 9th St': 'Kent Avenue',
                                         'Manhattan Bridge Bike Comprehensive': 'Manhattan Bridge',
                                         'Williamsburg Bridge Bike Path': 'Williamsburg Bridge',
                                         'Comprehensive Brooklyn Bridge Counter': 'Brooklyn Bridge'})

counts_total = counts[['date', 'counts']].groupby(['date']).sum().reset_index()
counts_total.columns = ['date', 'total']

counts = pd.merge(counts, counts_total, how = 'inner', on = 'date')
counts['%'] = counts['counts']/ counts['total']

# counts.to_csv(path + 'counts.csv', index = False)

counts['hover'] = '<b>' + counts['name'] + ': </b>' + counts['counts'].map('{:,.0f}'.format) + ' (' + counts['%'].map('{:.0%}'.format) + ')'

# counter_colors = {'Williamsburg Bridge':'#cdcc5d',
#                   'Manhattan Bridge': '#ff9e4a',
#                   'Brooklyn Bridge': '#ed665d',
#                   'Queensboro Bridge': '#67bf5c',
#                   'Staten Island Ferry':'#6dccda',
#                   'Prospect Park West': '#ed97ca',
#                   'Kent Ave btw N 8 St and N 9 St': '#729ece',      
#                   'Pulaski Bridge':'#ad8bc9',                 
#                   'Columbus Ave at 86 St': '#a2a2a2'}
counter_colors = {'Williamsburg Bridge':'rgba(205,204,93,0.5)',
                  'Manhattan Bridge': 'rgba(255,158,74,0.5)',
                  'Brooklyn Bridge': 'rgba(237,102,93,0.5)',
                  'Queensboro Bridge': 'rgba(103,191,92,0.5)',
                  'Staten Island Ferry':'rgba(109,204,218,0.5)',
                  'Prospect Park West': 'rgba(237,151,202,0.5)',
                  'Kent Avenue': 'rgba(114,158,206,0.5)',      
                  'Pulaski Bridge':'rgba(173,139,201,0.5)'}

hover_title = counts[['date', 'total']].groupby('date').first().reset_index()

fig = go.Figure()

fig = fig.add_trace(go.Scatter(x = hover_title['date'],
                               y = hover_title['total'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = '<b>Total Trips: </b>' + hover_title['total'].map('{:,.0f}'.format)))


# for counter, color in counter_colors.items():
#     fig = fig.add_trace(go.Scatter(name = counter,
#                                     x = counts.loc[counts['name'] == counter, 'date'],
#                                     y = counts.loc[counts['name'] == counter, 'counts'],
#                                     mode = 'lines',
#                                     stackgroup = 'one',
#                                     line = {'color': color,
#                                             'width': .5},
#                                     hoverinfo = 'text',
#                                     hovertext = counts.loc[counts['name'] == counter, 'hover']))

# for a 100% opacity fill chart with rgba colors
for counter, color in counter_colors.items():
    fig = fig.add_trace(go.Scatter(name = counter,
                                    x = counts.loc[counts['name'] == counter, 'date'],
                                    y = counts.loc[counts['name'] == counter, 'counts'],
                                    mode = 'none',
                                    stackgroup = 'one',
                                    groupnorm = '',
                                    orientation = 'v',
                                    fill = 'tonexty',
                                    fillcolor = color,
                                    hoverinfo = 'text',
                                    hovertext = counts.loc[counts['name'] == counter, 'hover']))
    
fig = fig.add_trace(go.Scatter(x = hover_title['date'],
                               y = hover_title['total'],
                               mode = 'none',
                               showlegend = False,
                               hoverinfo = 'text',
                               hovertext = '<b>Month: </b>' + hover_title['date'].map('{:%B %Y}'.format)))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Automatic Bicycle Counts</b>',
                           'font_size': 20,
                           'x': 0.5,
                           'xanchor':'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'orientation': 'h',
                            'title_text': '',
                            'font_size': 16,
                            'x': 0.5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120,
                            'l': 80,
                            'r': 40,
                            't': 180},
                  xaxis = {'title': {'text': '<b>Month</b>',
                                     'font_size': 14},
                           'tickfont_size': 12,
                           'tickformat':'%b %Y',
                           'dtick': 'M2',
                           'range':[min(counts['date'])-datetime.timedelta(days=15),max(counts['date'])+datetime.timedelta(days=15)],
                           'fixedrange': True,
                           'showgrid': False},
                  yaxis = {'title':{'text': '<b>Counts</b>',
                                    'font_size': 14},
                           'tickfont_size': 12,
                           'rangemode': 'tozero',
                           'fixedrange': True,
                           'showgrid': True},
                  font = {'family': 'Arial',
                          'color': 'black'},
                  hoverlabel = {'font_size': 14},
                  dragmode = False,
                  hovermode = 'x unified')

fig.add_annotation(text = 'Data Source: <a href="https://data.cityofnewyork.us/Transportation/Bicycle-Counts/uczf-rk3c" target="blank">NYC DOT</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/annotations/counts.csv" target="blank">Download Chart Data</a>',
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

# fig.write_html(path + 'counts.html',
#                 include_plotlyjs = 'cdn',
#                 config = {'displayModeBar': False})

# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/counts.html')


#%% CITI BIKE
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/bike/annotations/'
citibike = pd.read_csv(path + 'citibike.csv')
citibike['date']=[datetime.datetime.strptime(x,'%Y-%m') for x in citibike['YearMonth']]

# citibike['12M Rolling Avg'] = citibike['Avg Daily Rides'].rolling(window = 12).mean()
# citibike['Hover'] = '<b>Month: </b>' + citibike['date']+'<br><b>Average Daily Rides: </b>' + citibike['Avg Daily Rides'].map('{:,.0f}'.format) + '<br><b>12-Month Rolling Average: </b>' + citibike['12M Rolling Avg'].map('{:,.0f}'.format) + '<br><b>Fleet Size: </b>' + citibike['Fleet Size'].map('{:,.0f}'.format)

fig = go.Figure()

fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=citibike['date'],
                             y=citibike['Avg Daily Rides'],
                             showlegend=False,
                             hovertext=['<b>Month: </b>'+datetime.datetime.strftime(x,'%b %Y') for x in citibike['date']],
                             hoverinfo='text'))

fig = fig.add_trace(go.Bar(x = citibike['date'],
                           y = citibike['Avg Daily Rides'],
                           marker = {'color': 'rgba(114,158,206,0.5)'},
                           name = 'Average Daily Rides',
                           hoverinfo = 'text', 
                           hovertext ='<b>Average Daily Rides: </b>' + citibike['Avg Daily Rides'].map('{:,.0f}'.format)))

# fig = fig.add_trace(go.Scatter(x = citibike['Date'],
#                                y = citibike['12M Rolling Avg'], 
#                                marker = {'color': '#ff9e4a'},
#                                name = '12-Month Rolling Average',
#                                mode = 'lines',
#                                hoverinfo = 'none'))

# fig = fig.add_trace(go.Scatter(x = citibike['Date'],
#                                y = citibike['Fleet Size'], 
#                                marker = {'color': '#ed97ca'},
#                                name = 'Fleet Size',
#                                mode = 'lines',
#                                hoverinfo = 'none'))

fig=fig.add_trace(go.Scatter(name='Active Stations',
                             mode='lines',
                             x=citibike['date'],
                             y=citibike['Active Stations'],
                             yaxis='y2',
                             line={'color':'rgba(237,151,202,0.8)',
                                   'width':3},
                             hovertext=['<b>Active Stations: </b>'+'{:,.0f}'.format(x) for x in citibike['Active Stations']],
                             hoverinfo='text'))

fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=citibike['date'],
                             y=citibike['Avg Daily Rides'],
                             showlegend=False,
                             hovertext=['<b>Annual Membership: </b>'+'{:,.0f}'.format(x) for x in citibike['Annual Membership']],
                             hoverinfo='text'))

fig=fig.add_trace(go.Scatter(name='',
                             mode='none',
                             x=citibike['date'],
                             y=citibike['Avg Daily Rides'],
                             showlegend=False,
                             hovertext=['<b>Fleet Size: </b>'+'{:,.0f}'.format(x) for x in citibike['Fleet Size']],
                             hoverinfo='text'))
    
fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Citi Bike Statistics<b>',
                           'font_size': 20,
                           'x': .5,
                           'xanchor': 'center',
                           'y': .95,
                           'yanchor': 'top'},
                  legend = {'orientation': 'h',
                            'title_text':'',
                            'font_size': 16,
                            'x': .5,
                            'xanchor': 'center',
                            'y': 1,
                            'yanchor': 'bottom'},
                  margin = {'b': 120, 
                            'l': 80,
                            'r': 80,
                            't': 120},
                  xaxis = {'title':{'text':'<b>Month</b>',
                                    'font_size':14},
                           'tickfont_size':12,
                           'tickformat':'%b %Y',
                           'dtick':'M6',
                           'range':[min(citibike['date'])-datetime.timedelta(days=15),max(citibike['date'])+datetime.timedelta(days=15)],
                           'fixedrange':True,
                           'showgrid':False},
                  yaxis = {'title':{'text':'<b>Ridership</b>',
                                    'font_size':14},
                           'tickfont_size':12,
                           'rangemode':'tozero',
                           'fixedrange':True,
                           'showgrid':True},
                  yaxis2={'title':{'text':'<b>Stations</b>',
                                   'font_size':14},
                          'tickfont_size':12,
                          'side':'right',
                          'overlaying':'y',
                          'rangemode':'tozero',
                          'fixedrange':True,
                          'showgrid':False},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False,
                  hovermode = 'x unified')

fig.add_annotation(text = 'Data Source: <a href="https://ride.citibikenyc.com/system-data/operating-reports" target="blank">Citi Bike</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/annotations/citibike.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y=0,
                   yanchor='top',
                   yref='paper',
                   yshift=-100)
fig

# fig.write_html(path + 'citibike.html', include_plotlyjs='cdn', config={'displayModeBar':False})
# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/citibike.html')




#%% CMS Bike Frequency

path = 'C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/bike/annotations/'
cms=pd.read_csv('C:/Users/mayij/Desktop/Citywide_Mobility_Survey_-_Person_Survey_2019.csv',usecols=['weight','bike_freq'])
cms=cms.groupby(['bike_freq'],as_index=False).agg({'weight':['count','sum']}).reset_index(drop=True)
cms=cms[np.isin(cms['bike_freq'],[1,2,3,4,5,6])].reset_index(drop=True)
cms.columns=['bikefreq','count','weight']
cms['%'] = cms['weight'] / sum(cms['weight'])
cms['bikefreq'] = cms['bikefreq'].replace({1:'Once a Week or More',
                                           2:'Several Times a Month',
                                           3:'At Least Once a Month',
                                           4:'A Few Times a Year',
                                           5:'Never',
                                           6:'Physically Unable to Ride a Bike'})
# cms.to_csv(path + 'cmsfreq.csv',index=False)

cms=pd.read_csv(path+'cmsfreq.csv')
cms['hover'] = '<b>Frequency: </b>'+ cms['bikefreq'] + '<br><b>Persons: </b>' + cms['weight'].map('{:,.0f}'.format) +'<br><b>Percentage: </b>' + cms['%'].map('{:.0%}'.format)

cms_colors = {'Once a Week or More': 'rgba(237,102,93,0.8)',
              'Several Times a Month': 'rgba(255,158,74,0.8)',
              'At Least Once a Month': 'rgba(237,151,202,0.8)',
              'A Few Times a Year': 'rgba(173,139,201,0.8)',
              'Never': 'rgba(114,158,206,0.8)',
              'Physically Unable to Ride a Bike': 'rgba(162,162,162,0.8)'}

fig = go.Figure()

fig = fig.add_trace(go.Pie(labels = cms['bikefreq'],
                           values = cms['%'],
                           hole = .5,
                           sort = False,
                           direction = 'clockwise',
                           pull=0.05,
                           marker = {'colors': list(cms_colors.values())},
                           textinfo = 'text',
                           text= cms['%'].map('{:.0%}'.format),
                           textfont={'size':14},
                           hoverinfo = 'text',
                           hovertext = cms['hover']))

fig.update_layout(template = 'plotly_white',
                  title = {'text': '<b>Frequency of Bicycle Travel<b>',
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
                  margin = {'b': 40, 
                            'l': 80,
                            'r': 80,
                            't': 220},
                  hoverlabel = {'font_size': 14}, 
                  font = {'family': 'Arial',
                          'color': 'black'},
                  dragmode = False)

fig.add_annotation(text = 'Data Source: <a href="https://www1.nyc.gov/html/dot/html/about/citywide-mobility-survey.shtml" target="blank">NYC DOT 2019</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/annotations/cmsfreq.csv" target="blank">Download Chart Data</a>',
                   font_size = 14,
                   showarrow = False, 
                   x = 1, 
                   xanchor = 'right',
                   xref = 'paper',
                   y=0,
                   yanchor='top',
                   yref='paper',
                   yshift=0)
fig.add_annotation(text = f'Unweighted N = {cms["count"].sum():,.0f}<br>Weighted N = {cms["weight"].sum():,.0f}',
                   font_size = 14,
                   showarrow = False, 
                   x = .5,
                   y = .5)
                  
fig

# fig.write_html(path+'cmsfreq.html',
#                include_plotlyjs='cdn',
#                config={'displayModeBar':True,
#                        'displaylogo':False})
# print('Chart Available at: https://nycplanning.github.io/td-trends/bike/annotations/cmsfreq.html')


#%% CMS Bike Frequency

path = 'C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/bike/annotations/'
df=pd.DataFrame(columns=['purpose','count','weight'])
cms=pd.read_csv('C:/Users/mayij/Desktop/Citywide_Mobility_Survey_-_Person_Survey_2019.csv',usecols=['weight','bike_purpose_errands','bike_purpose_transit','bike_purpose_recreation','bike_purpose_commute','bike_purpose_appointment','bike_purpose_other'])
for i in ['errands','transit','recreation','commute','appointment','other']:
    df=df.append({'purpose':i,'count':cms.loc[cms['bike_purpose_'+i]==1,'weight'].count(),'weight':cms.loc[cms['bike_purpose_'+i]==1,'weight'].sum()},ignore_index=True)
df['%'] = df['weight'] / sum(df['weight'])
df['purpose']=['Errands','Transit','Recreation','Commute','Appointment','Other']
df['detail']=['To run errands','To connect to/from public transportation','For recreation/exercise',
              'To commute to work or school','To get to an appointment (e.g. doctor, meeting, conference)','Other']
df=df[['purpose','detail','count','weight','%']].sort_values(['weight'],ascending=False).reset_index(drop=True)
# df.to_csv(path + 'cmspurpose.csv',index=False)

cms=pd.read_csv(path+'cmspurpose.csv')
cms['hover'] = '<b>Purpose: </b>'+ cms['detail'] + '<br><b>Persons: </b>' + cms['weight'].map('{:,.0f}'.format) +'<br><b>Percentage: </b>' + cms['%'].map('{:.0%}'.format)

fig = go.Figure()

fig=fig.add_trace(go.Bar(name='Counts',
                         orientation='h',
                         y=cms['purpose'],
                         x=cms['weight'],
                         showlegend=False,
                         marker={'color':'rgba(109,204,218,0.8)'},
                         hovertext=cms['hover'],
                         hoverinfo='text'))

fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Reason for Riding a Bicycle</b><br>(Multiple Choice)',
           'font_size':20,
           'x':0.5,
           'xanchor':'center',
           'y':0.95,
           'yanchor':'top'},
    margin={'b':120,
            'l':80,
            'r':40,
            't':120},
    xaxis={'title':{'text':'<b>Persons</b>',
                    'font_size':14},
           'tickfont_size':12,
           'range':[0,1800000],
           'fixedrange':True,
           'showgrid':False},
    yaxis={'tickfont_size':14,
           'categoryorder':'total ascending',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False)

fig.add_annotation(
    text = 'Data Source: <a href="https://www1.nyc.gov/html/dot/html/about/citywide-mobility-survey.shtml" target="blank">NYC DOT 2019</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bike/annotations/cmspurpose.csv" target="blank">Download Chart Data</a>',
    font_size=14,
    showarrow=False,
    x=1,
    xanchor='right',
    xref='paper',
    y=0,
    yanchor='top',
    yref='paper',
    yshift=-80)

fig.write_html(path+'cmspurpose.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':True,
                       'displaylogo':False,
                       'modeBarButtonsToRemove':['select',
                                                 'lasso2d']})





