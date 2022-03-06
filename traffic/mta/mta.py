import xml.etree.ElementTree as et
import pandas as pd
import urllib.request
import shutil
import datetime

path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/traffic/mta/'

tlist=pd.read_csv(path+'tlist.csv')
tlist['time']=[datetime.datetime.strptime(x,'%A, %B %d, %Y').strftime('%Y%m%d') for x in tlist['time']]

for i in tlist['time']:
    url='http://web.mta.info/developers/data/bandt/tbta_plaza/PLAZA_DAILY_TRAFFIC_'+str(i)+'.xml'
    req=urllib.request.urlopen(url)
    file=open(path+'data/'+str(i)+'.xml','wb')
    shutil.copyfileobj(req,file)
    file.close()

df=pd.DataFrame(columns=['date','plazaid','cash','etc'])
for i in tlist['time']:
    try:
        xtree=et.parse(path+'data/'+str(i)+'.xml')
        xroot=xtree.getroot()
        tp=[]
        for j in xroot:
            for k in xroot[0]:
                tp=tp+[[j.get('Date'),k.get('id'),k.get('cash-count'),k.get('etc-count')]]
        tp=pd.DataFrame(tp,columns=['date','plazaid','cash','etc'])
        df=pd.concat([df,tp],axis=0,ignore_index=True)
    except:
        print(i+' error!')
df=df.drop_duplicates(keep='first').reset_index(drop=True)
df['yearmonth']=[str(x).split('/')[2]+str(x).split('/')[0] for x in df['date']]
df['plazaid']=pd.to_numeric(df['plazaid'])
df['cash']=pd.to_numeric(df['cash'])
df['etc']=pd.to_numeric(df['etc'])
df['total']=df['cash']+df['etc']
df=df.groupby(['yearmonth','plazaid'],as_index=False).agg({'cash':'sum','etc':'sum','total':'sum','date':'count'}).reset_index(drop=True)
df['dailyavg']=df['total']/df['date']
df=df.pivot(index='yearmonth',columns='plazaid',values='dailyavg')
df.to_csv(path+'mta.csv',index=True)





df=pd.read_csv('C:/Users/mayij/Desktop/Hourly_Traffic_on_Metropolitan_Transportation_Authority__MTA__Bridges_and_Tunnels__Beginning_2010.csv')
df['yearmonth']=[str(x).split('/')[2]+str(x).split('/')[0] for x in df['Date']]
df['Vehicles']=df['# Vehicles - E-ZPass']+df['# Vehicles - VToll']

k=df[df['Date']=='08/19/2018']
k=k.groupby(['Plaza ID'],as_index=False).agg({'# Vehicles - VToll':'sum',
                                                          '# Vehicles - E-ZPass':'sum'}).reset_index(drop=True)

k=df[df['Plaza ID']==22]
k.Direction.unique()


# df=df[df['Direction']=='I'].reset_index(drop=True)
df=df.groupby(['Plaza ID','yearmonth'],as_index=False).agg({'Vehicles':'sum'}).reset_index(drop=True)
df=df.pivot(index='yearmonth',columns='Plaza ID',values='Vehicles')
df.to_csv('C:/Users/mayij/Desktop/test.csv')
