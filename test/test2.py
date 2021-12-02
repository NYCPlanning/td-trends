import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import plotly.subplots as ps

pio.renderers.default = 'browser'
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/test/'
# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/test/'

# assign puma codes for each boro 
bronx = list(range(3700,3711))
brooklyn = list(range(4000,4019))
manhattan = list(range(3800,3811))
queens = list(range(4100,4115))
si = list(range(3900,3904))
nyc = bronx + brooklyn + manhattan + queens + si



# NYC COMMUTERS: DESTINATION
nyc_commuters=pd.read_csv(path+'nyc_commuters.csv',dtype=float,converters={'SERIALNO':str})

nyc_commuters['RES'] = np.select([nyc_commuters.PUMA.isin(bronx),
                                  nyc_commuters.PUMA.isin(brooklyn),
                                  nyc_commuters.PUMA.isin(manhattan),
                                  nyc_commuters.PUMA.isin(queens),
                                  nyc_commuters.PUMA.isin(si)],
                                 ['Bronx',
                                  'Brooklyn',
                                  'Manhattan',
                                  'Queens',
                                  'Staten Island'])

nyc_commuters['POW'] = np.select([nyc_commuters.POWPUMA.isin(bronx), 
                                  nyc_commuters.POWPUMA.isin(brooklyn),
                                  nyc_commuters.POWPUMA.isin(manhattan), 
                                  nyc_commuters.POWPUMA.isin(queens),  
                                  nyc_commuters.POWPUMA.isin(si)],
                                 ['Bronx', 
                                  'Brooklyn', 
                                  'Manhattan', 
                                  'Queens', 
                                  'Staten Island'],
                                 default = 'Region')

nyc_commuters['DEST'] = np.select([nyc_commuters.POW=='Region', 
                                  nyc_commuters.RES==nyc_commuters.POW],
                                 ['Region', 
                                  'Same Boro'],
                                 default='Other Boro')

nyc_commuters['MN'] = np.select([nyc_commuters['POW'] == 'Manhattan'],
                                ['Manhattan Bound'], 
                                default='Non-Manhattan Bound')

nyc_commuters['TT'] = np.select([nyc_commuters['JWMNP'] < 30, 
                                 nyc_commuters['JWMNP'] < 60],
                                ['Less Than 30 Mins', 
                                 '30 to 60 Mins'],
                                default='More Than 60 Mins')

tt = nyc_commuters[['RES', 'DEST', 'TT', 'PWGTP']].groupby(['RES', 'DEST', 'TT']).sum().reset_index()
tttotal=tt[['RES','DEST','PWGTP']].groupby(['RES','DEST']).sum().reset_index()
tttotal.columns=['RES','DEST','TOTAL']
tt=pd.merge(tt,tttotal,how='inner',on=['RES','DEST'])
tt['PCT']=tt['PWGTP']/tt['TOTAL']
tt.to_csv(path+'test2.csv',index=False)

# tt['HOVER']='<b>Residence: </b>'+dest['RES']+'<br><b>Workplace: </b>'+dest['DEST']+'<br><b>Commuters: </b>'+dest['PWGTP'].map('{:,.0f}'.format)+'<br><b>Percentage: </b>'+dest['PCT'].map('{:.0%}'.format)


# tt_fig = px.bar(tt, 
#                 x = 'RES', 
#                 y = 'PWGTP', 
#                 color = 'TT',
#                 facet_col = 'DEST',
#                 labels = {'RES':'Residence', 
#                           'PWGTP':'Number of Workers', 
#                           'DEST':'Destination', 
#                           'TT':'Travel Time'},
#                 category_orders={'TT': ['Less Than 30 Mins',
#                                         '30 to 60 Mins', 
#                                         'More Than 60 Mins'], 
#                                  'DEST':['Same Boro',
#                                          'Other Boro',
#                                          'Region']},
#                 title = 'Travel Time to Destination of Work by Borough of Residence for NYC Commuters')



boro=['Bronx','Brooklyn','Manhattan','Queens','Staten Island']
ttcat=['Less Than 30 Mins','30 to 60 Mins','More Than 60 Mins']

dfcolors={'Less Than 30 Mins':'#729ece',
          '30 to 60 Mins':'#ff9e4a',
          'More Than 60 Mins':'#67bf5c'}

fig=ps.make_subplots(rows=1,
                     cols=len(boro),
                     shared_yaxes=True,
                     subplot_titles=boro)

for i in range(0,1):
    for j in range(0,len(ttcat)):
        fig=fig.add_trace(go.Bar(name=ttcat[j],
                                 x=tt.loc[(tt['RES']==boro[i])&(tt['TT']==ttcat[j]),'DEST'],
                                 y=tt.loc[(tt['RES']==boro[i])&(tt['TT']==ttcat[j]),'PWGTP'],
                                 marker={'color':dfcolors[ttcat[j]]},
                                 legendgroup=ttcat[j],
                                 showlegend=True),
                      row=1,
                      col=i+1)
for i in range(1,len(boro)):
    for j in range(0,len(ttcat)):
        fig=fig.add_trace(go.Bar(name=ttcat[j],
                                 x=tt.loc[(tt['RES']==boro[i])&(tt['TT']==ttcat[j]),'DEST'],
                                 y=tt.loc[(tt['RES']==boro[i])&(tt['TT']==ttcat[j]),'PWGTP'],
                                 marker={'color':dfcolors[ttcat[j]]},
                                 legendgroup=ttcat[j],
                                 showlegend=False),
                      row=1,
                      col=i+1)
fig.update_layout(
    barmode='stack',
    template='plotly_white',
    title={'text':'<b>Destination of Work by Borough of Residence for NYC Commuters</b>',
           'font_size':20,
           'x':0.5,
           'xanchor':'center',
           'y':0.95,
           'yanchor':'top'},
    legend={'traceorder':'normal',
            'orientation':'h',
            'title_text':'',
            'font_size':16,
            'x':0.5,
            'xanchor':'center',
            'y':1,
            'yanchor':'bottom'},
    margin={'b':120,
            'l':80,
            'r':80,
            't':120},
    xaxis={'tickfont_size':14,
           'fixedrange':True,
           'showgrid':False},
    yaxis={'tickfont_size':12,
           'rangemode':'nonnegative',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False)
for i in range(0,len(boro)):
    fig.layout.annotations[i].update(y=-0.05,yanchor='top')
fig






fig.write_html(path+'test.html',
               include_plotlyjs='cdn',
               config={'displayModeBar':False})


