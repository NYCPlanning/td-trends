import geopandas as gpd
import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

taglist=[str(x)+str(y) for x in ['m','t','w','r','f','s','u'] for y in [str(x)[11:13]+str(x)[14:16] for x in pd.date_range('00:00','23:30',freq='30min')]]
taglistcat=[str(x)+str(y)+'cat' for x in ['m','t','w','r','f','s','u'] for y in [str(x)[11:13]+str(x)[14:16] for x in pd.date_range('00:00','23:30',freq='30min')]]

ct=gpd.read_file('C:/Users/mayij/Desktop/parking/nyct2020wi.shp')
ct.crs=2263
ct=ct.to_crs(4326)
ct=ct[['GEOID','geometry']].reset_index(drop=True)

ctclipped=gpd.read_file('C:/Users/mayij/Desktop/parking/nyct2020.shp')
ctclipped.crs=2263
ctclipped=ctclipped.to_crs(4326)
ctclipped=ctclipped[['GEOID','geometry']].reset_index(drop=True)

df=pd.read_csv('C:/Users/mayij/Desktop/parking/CTTIMEPKSPACES.csv',dtype=str,converters={'total':float})
df['GEOID']=df['geoid'].copy()
df['day']=[str(x).split(' ')[0] for x in df['time']]
df['day']=np.where(df['day']=='Monday','m',
          np.where(df['day']=='Tuesday','t',
          np.where(df['day']=='Wednesday','w',
          np.where(df['day']=='Thursday','r',
          np.where(df['day']=='Friday','f',
          np.where(df['day']=='Saturday','s',
          np.where(df['day']=='Sunday','u','Other')))))))
df['time']=[str(x).split(' ')[1].replace(':','') for x in df['time']]
df['time']=df['day']+df['time']
df['total'].describe(percentiles=np.arange(0.2,1,0.2))
dfcat=df.copy()
dfcat['totalcat']=np.where(dfcat['total']<=250,'<=250',
                  np.where(dfcat['total']<=500,'251-500',
                  np.where(dfcat['total']<=750,'501-750',
                  np.where(dfcat['total']<=1000,'751-1000',
                           '>1000'))))
df=df.pivot(index='GEOID',columns='time',values='total').reset_index(drop=False)
df=df[['GEOID']+taglist].reset_index(drop=True)
dfcat=dfcat.pivot(index='GEOID',columns='time',values='totalcat').reset_index(drop=False)
dfcat=dfcat[['GEOID']+taglist].reset_index(drop=True)
dfcat.columns=['GEOID']+taglistcat
df=pd.merge(ctclipped,df,how='left',on='GEOID')
df=df.fillna(0)
df=pd.merge(df,dfcat,how='left',on='GEOID')
df=df.fillna('<=250')
df=df[['GEOID']+taglist+taglistcat+['geometry']].reset_index(drop=True)
df.to_file('C:/Users/mayij/Desktop/parking/onstparking.geojson',driver='GeoJSON')
