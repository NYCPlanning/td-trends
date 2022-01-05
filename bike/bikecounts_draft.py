#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 09:55:30 2022

@author: Work
"""
import pandas as pd
from datetime import datetime

parser = lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p') # 8/31/2012  12:00:00 AM                 
counts = pd.read_csv('/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/bicycle_counts.csv', parse_dates = ['date'], date_parser = parser)

counters = pd.read_csv('/Users/Work/OneDrive - NYC O365 HOSTED/Data/Travel Trends Update/Dec 2021/bicycle_counters.csv', usecols = ['name', 'site', 'latitude','longitude'])
# counters = counters[['name', 'site', 'latitude','longitude']]

counters_map = {100057316: '8th Ave at 50th St',
                100057319: 'Amsterdam Ave at 86th St',
                100057318: 'Broadway at 50th St',
                100010022: 'Brooklyn Bridge Bike Path',
                100057320: 'Columbus Ave at 86th St',
                100009428: 'Ed Koch Queensboro Bridge Shared Path',
                100010019: 'Kent Ave btw North 8th St and North 9th St',
                100062893: 'Manhattan Bridge Bike Comprehensive',
                100009425: 'Prospect Park West',
                100010018: 'Pulaski Bridge',
                100010017: 'Staten Island Ferry',
                100009427: 'Williamsburg Bridge Bike Path'}

counts = counts[counts.site.isin(list(counters_map.keys()))]

counts['date'] = pd.to_datetime(counts['date']).dt.date
counts = counts['site', 'date', 'counts'].groupby(['site','date']).sum().reset_index()



counts = counts.merge(counters, how='left', on='site')


time = counts.groupby(['name', 'site']).agg({'date': ['min','max'], 'counts':'sum'})


counts['name'].value_counts()