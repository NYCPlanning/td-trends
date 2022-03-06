library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'traffic/PANYNJ Bridges&Tunnels Inbound.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(paste0(YearMonth,'01'),'%Y%m%d')) %>%
  filter((Location=='All Crossings')&(Type %in% c('Automobiles','Trucks'))) %>%
  spread(key=Type,value=Value) %>%
  select(Date,Automobiles,Trucks)


dfcolors=c('Automobiles'='rgba(255,158,74,0.6)',
           'Trucks'='rgba(103,191,92,0.6)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['Trucks']],
            showlegend=F,
            hovertext=paste0('<b>Month: </b>',format(df[['Date']],'%b %Y')),
            hoverinfo='text')
p=p %>%
  add_trace(name='Automobiles',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Automobiles']],
            line=list(color=dfcolors['Automobiles'],
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>Automobiles: </b>',format(df[['Automobiles']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  add_trace(name='Trucks',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Trucks']],
            yaxis='y2',
            line=list(color=dfcolors['Trucks'],
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>Trucks: </b>',format(df[['Trucks']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>PANYNJ Monthly Inbound Crossings</b>'),
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
                    dtick='M6',
                    range=c(min(df[['Date']])-15,max(df[['Date']])+15),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Number of Automobiles</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         yaxis2=list(title=list(text='<b>Number of Trucks</b>',
                                font=list(size=14)),
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
  add_annotations(text='Data Source: <a href="https://www.panynj.gov/bridges-tunnels/en/traffic---volume-information---b-t.html" target="blank">PANYNJ</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/traffic/PANYNJ Bridges&Tunnels Inbound.csv" target="blank">Download Chart Data</a>',
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
htmlwidgets::saveWidget(p,paste0(path,'traffic/PANYNJTruck.html'))




