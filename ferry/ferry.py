import pandas as pd
import numpy as np
import geopandas as gpd
import shapely
import os



pd.set_option('display.max_columns', None)
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'



# Private Ferry
pfop=pd.DataFrame(columns=['id'])
pfld=pd.DataFrame(columns=['id'])

for i in range(2013,2018):
    for j in range(1,13):
        tp=[x for x in os.listdir(path+'ferry/Private Ferry Monthly Ridership/'+str(i)) if x.startswith(str(j).zfill(2))][0]
        tp=pd.read_excel(path+'ferry/Private Ferry Monthly Ridership/'+str(i)+'/'+tp,sheet_name='Monthly Totals')
        tp=tp.iloc[:,0:2].reset_index(drop=True)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        tp=tp[pd.notna(tp['id'])].reset_index(drop=True)
        tpop=tp[tp['id']=='Ridership by Operator'].index[0]
        tpld=tp[tp['id']=='Ridership by Landing'].index[0]
        tpop=tp[tpop+1:tpld].reset_index(drop=True)
        pfop=pd.merge(pfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        pfld=pd.merge(pfld,tpld,how='outer',on='id')

for i in range(2018,2021):
    for j in range(1,13):
        tp=[x for x in os.listdir(path+'ferry/Private Ferry Monthly Ridership/'+str(i)) if x.endswith(str(j).zfill(2)+'.xlsx')][0]
        tp=pd.read_excel(path+'ferry/Private Ferry Monthly Ridership/'+str(i)+'/'+tp,sheet_name='Monthly Totals')
        tp=tp.iloc[:,0:2].reset_index(drop=True)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        tp=tp[pd.notna(tp['id'])].reset_index(drop=True)
        tpop=tp[tp['id']=='Ridership by Operator'].index[0]
        tpld=tp[tp['id']=='Ridership by Landing'].index[0]
        tpop=tp[tpop+1:tpld].reset_index(drop=True)
        pfop=pd.merge(pfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        pfld=pd.merge(pfld,tpld,how='outer',on='id')

for i in range(2021,2022):
    for j in range(1,5):
        tp=[x for x in os.listdir(path+'ferry/Private Ferry Monthly Ridership/'+str(i)) if x.endswith(str(j).zfill(2)+'.xlsx')][0]
        tp=pd.read_excel(path+'ferry/Private Ferry Monthly Ridership/'+str(i)+'/'+tp,sheet_name='Monthly Totals')
        tp=tp.iloc[:,0:2].reset_index(drop=True)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        tp=tp[pd.notna(tp['id'])].reset_index(drop=True)
        tpop=tp[tp['id']=='Ridership by Operator'].index[0]
        tpld=tp[tp['id']=='Ridership by Landing'].index[0]
        tpop=tp[tpop+1:tpld].reset_index(drop=True)
        pfop=pd.merge(pfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        pfld=pd.merge(pfld,tpld,how='outer',on='id')

for i in range(2021,2022):
    for j in range(6,8):
        tp=[x for x in os.listdir(path+'ferry/Private Ferry Monthly Ridership/'+str(i)) if x.endswith(str(j).zfill(2)+'.xlsx')][0]
        tp=pd.read_excel(path+'ferry/Private Ferry Monthly Ridership/'+str(i)+'/'+tp,sheet_name='Monthly Totals')
        tp=tp.iloc[:,1:3].reset_index(drop=True)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        tp=tp[pd.notna(tp['id'])].reset_index(drop=True)
        tpop=tp[tp['id']=='Ridership by Operator'].index[0]
        tpld=tp[tp['id']=='Ridership by Landing'].index[0]
        tpop=tp[tpop+1:tpld].reset_index(drop=True)
        pfop=pd.merge(pfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        pfld=pd.merge(pfld,tpld,how='outer',on='id')

for i in range(2021,2022):
    for j in range(8,11):
        tp=[x for x in os.listdir(path+'ferry/Private Ferry Monthly Ridership/'+str(i)) if x.endswith(str(j).zfill(2)+'.xlsx')][0]
        tp=pd.read_excel(path+'ferry/Private Ferry Monthly Ridership/'+str(i)+'/'+tp,sheet_name='Monthly Totals')
        tp=tp.iloc[:,1:3].reset_index(drop=True)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        tp=tp[pd.notna(tp['id'])].reset_index(drop=True)
        tpop=tp[tp['id']=='Ridership by Operator'].index[0]
        tpld=tp[tp['id']=='Ridership by (DOT-Owned) Landing'].index[0]
        tpop=tp[tpop+1:tpld].reset_index(drop=True)
        pfop=pd.merge(pfop,tpop,how='outer',on='id')

pfop=pfop.sort_values('id').reset_index(drop=True)
pfop=pfop.transpose().reset_index(drop=False)
pfop.columns=['yearmonth']+list(pfop.iloc[0,1:])
pfop=pfop[1:].reset_index(drop=True)
pfop.to_csv(path+'ferry/PrivateFerryByOperator.csv',index=False,na_rep=0)

pfld=pfld.sort_values('id').reset_index(drop=True)
pfld=pfld.transpose().reset_index(drop=False)
pfld.columns=['yearmonth']+list(pfld.iloc[0,1:])
pfld=pfld[1:].reset_index(drop=True)
pfld.to_csv(path+'ferry/PrivateFerryByLanding.csv',index=False,na_rep=0)



# Staten Island Ferry
sif=pd.DataFrame(columns=['id'])
for i in range(2012,2016):
    for j in range(1,13):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.startswith(str(j).zfill(2))][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

for i in range(2016,2017):
    for j in list(range(1,8))+list(range(9,13)):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.startswith(str(j).zfill(2))][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

for i in range(2017,2019):
    for j in range(1,13):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.startswith(str(j).zfill(2))][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

for i in range(2019,2020):
    for j in range(1,13):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.endswith(str(j).zfill(2)+'.xls')][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

for i in range(2020,2021):
    for j in range(1,13):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.endswith(str(j).zfill(2)+'.xlsx')][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

for i in range(2021,2022):
    for j in range(1,5):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.endswith(str(j).zfill(2)+'.xlsx')][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

for i in range(2021,2022):
    for j in range(5,11):
        tp=[x for x in os.listdir(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)) if x.endswith(str(j).zfill(2)+'.xls')][0]
        tp=pd.read_excel(path+'ferry/Staten Island Ferry Passenger Counts - by Month/'+str(i)+'/'+tp,sheet_name='TOTALS',skiprows=4)
        tp=tp.loc[tp['Date']=='TOTALS:',['WHT','STG']].reset_index(drop=True)
        tp=tp.transpose().reset_index(drop=False)
        tp.columns=['id',str(i)+str(j).zfill(2)]
        sif=pd.merge(sif,tp,how='outer',on='id')

sif=sif.sort_values('id').reset_index(drop=True)
sif=sif.transpose().reset_index(drop=False)
sif.columns=['yearmonth']+list(sif.iloc[0,1:])
sif=sif[1:].reset_index(drop=True)
sif.to_csv(path+'ferry/SIFRidership.csv',index=False,na_rep=0)



pfop=pd.read_csv(path+'ferry/PrivateFerryByOperator.csv')
pfop=pfop.drop(['Total'],axis=1).reset_index(drop=True)
sif=pd.read_csv(path+'ferry/SIFRidership.csv')
sif['Staten Island Ferry']=sif['STG']+sif['WHT']
sif=sif[['yearmonth','Staten Island Ferry']].reset_index(drop=True)
ferryop=pd.merge(pfop,sif,how='left',on='yearmonth')
ferryop.to_csv(path+'ferry/FerryByOperator.csv',index=False)



ferryld=pd.read_csv(path+'ferry/ferryld.csv')
ferryld['YM202110'].describe(percentiles=np.arange(0.2,1,0.2))
ferryld['cat']=np.where(ferryld['YM202110']>=500000,'>500000',
               np.where(ferryld['YM202110']>=100000,'100000~499999',
               np.where(ferryld['YM202110']>=50000,'50000~99999',
               np.where(ferryld['YM202110']>=10000,'10000~49999',
                        '<10000'))))
ferryld=gpd.GeoDataFrame(ferryld,geometry=[shapely.geometry.Point(x,y) for x,y in zip(ferryld['Long'],ferryld['Lat'])],crs=4326)
ferryld.to_file(path+'ferry/ferryld.geojson',driver='GeoJSON')




