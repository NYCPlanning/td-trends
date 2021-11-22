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



df=pd.read_csv(path+'subway/Subway Ridership 2008-2020.csv')
df=df[['CmplxID','Boro','CmplxName','Routes','Lat','Long','Annu2015','Annu2019','Annu2020','Notes']].reset_index(drop=True)
df['Notes']=np.where(pd.isna(df['Notes']),'',df['Notes'])
df['Pct1519']=(df['Annu2019']-df['Annu2015'])/df['Annu2015']
df['Pct1519'].describe(percentiles=np.arange(0.2,1,0.2))
df['Pct1519Cat']=np.where(df['Pct1519']>0.15,'>15%',
                 np.where(df['Pct1519']>=0.05,'5%~15%',
                 np.where(df['Pct1519']>=-0.05,'-5%~5%',
                 np.where(df['Pct1519']>=-0.15,'-15%~-5%',
                          '<-15%'))))
df=gpd.GeoDataFrame(df,geometry=[shapely.geometry.Point(x,y) for x,y in zip(df['Long'],df['Lat'])],crs=4326)
df.to_file(path+'subway/subway1519.geojson',driver='GeoJSON')
