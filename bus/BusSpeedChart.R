library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'bus/BusSpeed2015-2021.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(paste0(Month,'-01'),'%Y-%m-%d')) %>%
  filter(Date>=as.Date('2019-01-01','%Y-%m-%d'))

dfcolors=c('Bronx'='rgba(114,158,206,0.8)',
           'Brooklyn'='rgba(255,158,74,0.8)',
           'Manhattan'='rgba(103,191,92,0.8)',
           'Queens'='rgba(237,102,93,0.8)',
           'Staten Island'='rgba(173,139,201,0.8)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['Manhattan']],
            showlegend=F,
            hovertext=paste0('<b>Month: </b>',format(df[['Date']],'%b %Y')),
            hoverinfo='text')
for (i in c('Bronx','Brooklyn','Manhattan','Queens','Staten Island')){
  p=p %>%
    add_trace(name=i,
              type='scatter',
              mode='lines+markers',
              x=df[['Date']],
              y=df[[i]],
              line=list(color=dfcolors[i],
                        width=2),
              marker=list(color=dfcolors[i],
                          size=6),
              showlegend=T,
              hovertext=paste0('<b>',i,': </b>',format(round(df[[i]],2),trim=T,nsmall=2)),
              hoverinfo='text')
}
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b> Monthly Bus Speed</b>'),
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
                     t=150),
         xaxis=list(title=list(text='<b>Month</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    dtick='M2',
                    range=c(min(df[['Date']])-15,max(df[['Date']])+15),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Speed (mph)</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         hoverlabel=list(font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="http://busdashboard.mta.info/" target="blank">MTA</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/BusSpeed2015-2021.csv" target="blank">Download Chart Data</a>',
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
htmlwidgets::saveWidget(p,paste0(path,'bus/BusSpeedChart.html'))





