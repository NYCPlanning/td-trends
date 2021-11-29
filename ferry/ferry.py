import pandas as pd
import os



pd.set_option('display.max_columns', None)
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



dfop=pd.DataFrame(columns=['id'])
dfld=pd.DataFrame(columns=['id'])

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
        dfop=pd.merge(dfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        dfld=pd.merge(dfld,tpld,how='outer',on='id')

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
        dfop=pd.merge(dfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        dfld=pd.merge(dfld,tpld,how='outer',on='id')

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
        dfop=pd.merge(dfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        dfld=pd.merge(dfld,tpld,how='outer',on='id')

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
        dfop=pd.merge(dfop,tpop,how='outer',on='id')
        tpld=tp[tpld+1:].reset_index(drop=True)
        dfld=pd.merge(dfld,tpld,how='outer',on='id')




dfop.to_csv(path+'ferry/')