library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'traffic/MonthlyBTTraffic.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(paste0(YearMonth,'01'),'%Y%m%d'))

dfcolors=c('MTA'='rgba(173,139,201,0.8)',
           'PANYNJ'='rgba(103,191,92,0.8)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['PANYNJ']],
            showlegend=F,
            hovertext=paste0('<b>Month: </b>',format(df[['Date']],'%b %Y')),
            hoverinfo='text')
p=p %>%
  add_trace(name='MTA Bridges & Tunnels',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['MTA']],
            line=list(color=dfcolors['MTA'],
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>MTA: </b>',format(df[['MTA']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  add_trace(name='PANYNJ Bridges & Tunnels (Inbound Only)',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['PANYNJ']],
            line=list(color=dfcolors['PANYNJ'],
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>PANYNJ Inbound: </b>',format(df[['PANYNJ']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Monthly Bridges & Tunnels Traffic Volume</b>'),
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
                     r=40,
                     t=120),
         xaxis=list(title=list(text='<b>Month</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    tickformat='%b %Y',
                    dtick='M6',
                    range=c(min(df[['Date']])-15,max(df[['Date']])+15),                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Vehicles (Including Trucks & Buses)</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         hoverlabel=list(bgcolor='rgba(255,255,255,0.95)',
                         bordercolor='rgba(0,0,0,0.1)',
                         font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://new.mta.info/transparency/board-and-committee-meetings" target="blank">MTA</a>; <a href="https://www.panynj.gov/bridges-tunnels/en/traffic---volume-information---b-t.html" target="blank">PANYNJ</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/traffic/MonthlyBTTraffic.csv" target="blank">Download Chart Data</a>',
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
  config(displayModeBar=T,
         displaylogo=F)
p
htmlwidgets::saveWidget(p,paste0(path,'traffic/MonthlyBTTraffic.html'))




