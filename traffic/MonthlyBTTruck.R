library(tidyverse)
library(plotly)

path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'traffic/MonthlyBTTruck.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(paste0(YearMonth,'01'),'%Y%m%d'))


dfcolors=c('Auto'='rgba(162,162,162,0.8)',
           'Truck'='rgba(237,102,93,0.8)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['Truck']],
            showlegend=F,
            hovertext=paste0('<b>Month: </b>',format(df[['Date']],'%b %Y')),
            hoverinfo='text')
p=p %>%
  add_trace(name='Auto',
            type='scatter',
            mode='lines+markers',
            x=df[['Date']],
            y=df[['Auto']],
            line=list(color=dfcolors['Auto'],
                      width=3),
            marker=list(color=dfcolors['Auto'],
                        size=8),
            showlegend=T,
            hovertext=paste0('<b>Auto: </b>',format(df[['Auto']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  add_trace(name='Truck',
            type='scatter',
            mode='lines+markers',
            x=df[['Date']],
            y=df[['Truck']],
            yaxis='y2',
            line=list(color=dfcolors['Truck'],
                      width=3),
            marker=list(color=dfcolors['Truck'],
                        size=8),
            showlegend=T,
            hovertext=paste0('<b>Truck: </b>',format(df[['Truck']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Monthly Bridges and Tunnels Truck Traffic</b>'),
                    font=list(size=20),
                    x=0.5,
                    xanchor='center',
                    y=0.95,
                    yanchor='top'),
         legend=list(orientation='h',
                     title=list(text=''),
                     font=list(size=16),
                     x=0.5,
                     xanchor='center',
                     y=1,
                     yanchor='bottom'),
         margin=list(b=120,
                     l=80,
                     r=80,
                     t=120),
         xaxis=list(title=list(text='<b>Month</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    tickformat='%b %Y',
                    dtick='M2',
                    range=c(min(df[['Date']])-15,max(df[['Date']])+15),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Number of Automobiles</b>',
                               font=list(size=14,
                                         color=dfcolors['Auto'])),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         yaxis2=list(title=list(text='<b>Number of Trucks</b>',
                                font=list(size=14,
                                          color=dfcolors['Truck'])),
                     tickfont=list(size=12),
                     side='right',
                     overlaying='y',
                     rangemode='tozero',
                     fixedrange=T,
                     showgrid=F,
                     zeroline=F),
         hoverlabel=list(font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://new.mta.info/transparency/board-and-committee-meetings" target="blank">MTA</a>; <a href="https://www.panynj.gov/bridges-tunnels/en/traffic---volume-information---b-t.html" target="blank">PANYNJ</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/traffic/MonthlyBTTruck.csv" target="blank">Download Chart Data</a>',
                  font=list(size=14),
                  showarrow=F,
                  x=1,
                  xanchor='right',
                  xref='paper',
                  y=0,
                  yanchor='top',
                  yref='paper',
                  yshift=-80)
p=p %>%
  config(displayModeBar=F)
p
htmlwidgets::saveWidget(p,paste0(path,'traffic/MonthlyBTTruck.html'))




