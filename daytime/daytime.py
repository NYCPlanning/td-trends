import pandas as pd
import numpy as np
import geopandas as gpd
import shapely
import os



pd.set_option('display.max_columns', None)
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'



df=gpd.read_file(path+'daytime/daytime.geojson')
df.crs=4326

df['daypop'].describe(percentiles=np.arange(0.2,1,0.2))
df['cat']=np.where(df['daypop']<20000,'<=20k',
          np.where(df['daypop']<=40000,'21k~40k',
          np.where(df['daypop']<=60000,'41k~60k',
          np.where(df['daypop']<=80000,'61k~80k',
                    '>80k'))))

df['percdpl'].describe(percentiles=np.arange(0.2,1,0.2))
df['catl']=np.where(df['percdpl']>=0.1,'10%~28%',
           np.where(df['percdpl']>=0.05,'5%~9%',
           np.where(df['percdpl']>=-0.02,'-2%~4%',
           np.where(df['percdpl']>=-0.16,'-16%~-3%',
                    '-37%~-17%'))))
df['catm']=np.where(df['percdpm']>=0.1,'10%~28%',
           np.where(df['percdpm']>=0.05,'5%~9%',
           np.where(df['percdpm']>=-0.02,'-2%~4%',
           np.where(df['percdpm']>=-0.16,'-16%~-3%',
                    '-37%~-17%'))))
df['cath']=np.where(df['percdph']>=0.1,'10%~28%',
           np.where(df['percdph']>=0.05,'5%~9%',
           np.where(df['percdph']>=-0.02,'-2%~4%',
           np.where(df['percdph']>=-0.16,'-16%~-3%',
                    '-37%~-17%'))))
df['cate']=np.where(df['percdpe']>=0.1,'10%~28%',
           np.where(df['percdpe']>=0.05,'5%~9%',
           np.where(df['percdpe']>=-0.02,'-2%~4%',
           np.where(df['percdpe']>=-0.16,'-16%~-3%',
                    '-37%~-17%'))))






# df['daypopdiffl']=df['daypopl']-df['daypop']
# df['daypopdiffl'].describe(percentiles=np.arange(0.2,1,0.2))
# df['catl']=np.where(df['daypopdiffl']<500,'<=500',
#            np.where(df['daypopdiffl']<=1000,'501~1000',
#            np.where(df['daypopdiffl']<=1500,'1001~1500',
#            np.where(df['daypopdiffl']<=2000,'1501~2000',
#                     '>2000'))))

# df['daypopdiffm']=df['daypopm']-df['daypop']
# df['daypopdiffm'].describe(percentiles=np.arange(0.2,1,0.2))
# df['catm']=np.where(df['daypopcdiffm']<500,'<=500',
#            np.where(df['daypopcdiffm']<=1000,'501~1000',
#            np.where(df['daypopcdiffm']<=1500,'1001~1500',
#            np.where(df['daypopcdiffm']<=2000,'1501~2000',
#                     '>2000'))))

# df['daypopdiffh']=df['daypoph']-df['daypop']
# df['daypopdiffh'].describe(percentiles=np.arange(0.2,1,0.2))
# df['cath']=np.where(df['daypopcdiffh']<500,'<=500',
#            np.where(df['daypopcdiffh']<=1000,'501~1000',
#            np.where(df['daypopcdiffh']<=1500,'1001~1500',
#            np.where(df['daypopcdiffh']<=2000,'1501~2000',
#                     '>2000'))))

# df['daypopdiffe']=df['daypope']-df['daypop']
# df['daypopdiffe'].describe(percentiles=np.arange(0.2,1,0.2))
# df['cate']=np.where(df['daypopcdiffe']<500,'<=500',
#            np.where(df['daypopcdiffe']<=1000,'501~1000',
#            np.where(df['daypopcdiffe']<=1500,'1001~1500',
#            np.where(df['daypopcdiffe']<=2000,'1501~2000',
#                     '>2000'))))

df.to_file(path+'daytime/daytime.geojson',driver='GeoJSON')


k=pd.concat([df['percdpl'],df['percdpm'],df['percdph'],df['percdpe']],axis=0,ignore_index=True)
k.describe(percentiles=np.arange(0.2,1,0.2))
k.hist(bins=100)


