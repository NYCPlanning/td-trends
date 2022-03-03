import pandas as pd
import geopandas as gpd
import shapely
import numpy as np

import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go


path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
pd.set_option('display.max_columns', None)
pio.renderers.default='browser'



df=pd.read_csv(path+'subway/SubwayRidership2008-2020.csv')
df=df[['CmplxID','Boro','CmplxName','Routes','Lat','Long','Annu2015','Annu2016','Annu2017','Annu2018',
       'Annu2019','Annu2020','Notes']].reset_index(drop=True)
df['Notes']=np.where(pd.isna(df['Notes']),'',df['Notes'])
df['Pct1519']=(df['Annu2019']-df['Annu2015'])/df['Annu2015']
df['Pct1519'].describe(percentiles=np.arange(0.2,1,0.2))
df['Pct1519Cat']=np.where(df['Pct1519']>0.15,'>15%',
                 np.where(df['Pct1519']>=0.05,'5%~15%',
                 np.where(df['Pct1519']>=-0.05,'-5%~5%',
                 np.where(df['Pct1519']>=-0.15,'-15%~-5%',
                          '<-15%'))))
df=gpd.GeoDataFrame(df,geometry=[shapely.geometry.Point(x,y) for x,y in zip(df['Long'],df['Lat'])],crs=4326)
df.to_file(path+'subway/annual1519.geojson',driver='GeoJSON')




df=pd.read_csv(path+'subway/subway2019_2021_September Avg weekday.csv')
df.columns=['CmplxID','Boro','CmplxName','Routes','Lat','Long','Sept2019','Sept2020','Sept2021','Notes']
df['Notes']=np.where(pd.isna(df['Notes']),'',df['Notes'])
df['Pct20']=df['Sept2020']/df['Sept2019']
df['Pct20'].describe(percentiles=np.arange(0.2,1,0.2))
df['Pct21']=df['Sept2021']/df['Sept2019']
df['Pct21'].describe(percentiles=np.arange(0.2,1,0.2))
df['Pct20Cat']=np.where(df['Pct20']>=0.6,'>=60%',
               np.where(df['Pct20']>=0.5,'50%~59%',
               np.where(df['Pct20']>=0.4,'40%~49%',
               np.where(df['Pct20']>=0.3,'30%~39%',
                        '<30%'))))
df['Pct21Cat']=np.where(df['Pct21']>=0.6,'>=60%',
               np.where(df['Pct21']>=0.5,'50%~59%',
               np.where(df['Pct21']>=0.4,'40%~49%',
               np.where(df['Pct21']>=0.3,'30%~39%',
                        '<30%'))))
df=gpd.GeoDataFrame(df,geometry=[shapely.geometry.Point(x,y) for x,y in zip(df['Long'],df['Lat'])],crs=4326)
df.to_file(path+'subway/septwkd.geojson',driver='GeoJSON')
