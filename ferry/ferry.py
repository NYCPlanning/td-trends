import pandas as pd

path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=pd.read_excel(path+'ferry/Private Ferry Monthly Ridership/2020/PrivateFerryRidership_2020_03.xlsx',sheet_name='Monthly Totals')
df=df[pd.notna(df['Monthly Totals'])].reset_index(drop=True)
df=df[df['Monthly Totals']!='Total'].reset_index(drop=True)
n=df[df['Monthly Totals']=='Ridership by Landing'].index[0]
df=df[n:].reset_index(drop=True)
