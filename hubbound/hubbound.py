import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go



pio.renderers.default = "browser"
pd.set_option('display.max_columns', None)
path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'



df=pd.read_excel(path+'hub bound/Hub Bound Compilation From Regional planning folder.xlsx',sheet_name='SUMMARY')

fig=go.Figure()
dfcolors={'PATH':'#729ece',
          'NJT':'#ff9e4a',
          'LIRR':'#67bf5c',
          'MNR':'#ed665d',
          'AMTRAK':'#a8786e',
          'NJ BUS':'#ad8bc9'}
fig=fig.add_trace(go.Scattergl(name='',
                               x=df['YEAR'],
                               y=df['AMTRAK'],
                               opacity=0,
                               showlegend=False,
                               hovertext=['<b>'+str(x)+'</b>' for x in df['YEAR']],
                               hoverinfo='text'))
for i in ['PATH','NJT','LIRR','MNR','AMTRAK','NJ BUS']:
    fig=fig.add_trace(go.Scattergl(name=i,
                                   mode='lines+markers',
                                   x=df['YEAR'],
                                   y=df[i],
                                   line={'color':dfcolors[i],
                                         'width':2},
                                   hovertemplate='%{y:,0f}'))
fig.update_layout(
    template='plotly_white',
    title={'text':'<b>Daily Entries to the Manhattan Hub (2000-2019)</b>',
           'font_size':20,
           'x':0.5,
           'xanchor':'center',
           'y':0.98,
           'yanchor':'top'},
    legend={'orientation':'h',
            'title_text':'',
            'font_size':16,
            'x':0.5,
            'xanchor':'center',
            'y':1,
            'yanchor':'bottom'},
    xaxis={'title':{'text':'<b>Year</b>',
                    'font_size':14},
           'tickfont_size':12,
           'dtick':'M12',
           'range':[min(df['YEAR'])-0.5,max(df['YEAR'])+0.5],
           'fixedrange':True,
           'showgrid':False},
    yaxis={'title':{'text':'<b>Daily Entries</b>',
                    'font_size':14},
           'tickfont_size':12,
           'rangemode':'nonnegative',
           'fixedrange':True,
           'showgrid':True},
    hoverlabel={'font_size':14},
    font={'family':'Arial',
          'color':'black'},
    dragmode=False,
    hovermode='x unified',
    )
fig.write_html(path+'hub bound/hubbound.html',
               include_plotlyjs='cdn',
               config={'displaylogo':False,'modeBarButtonsToRemove':['select2d','lasso2d']})















