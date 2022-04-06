library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'tlc/TLC_Monthly.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(paste0(YearMonth,'-01'),'%Y-%m-%d'))

dfcolors=c('Yellow Taxi'='rgba(255,158,74,0.6)',
           'Green Taxi'='rgba(103,191,92,0.6)',
           'For-Hire Vehicle'='rgba(114,158,206,0.6)',
           'Unique Drivers'='rgba(173,139,201,0.8)',
           'Unique Vehicles'='rgba(237,102,93,0.8)')

p=plot_ly()
for (i in c('Unique Vehicles','Unique Drivers')){
  p=p %>%
    add_trace(name=i,
              type='scatter',
              mode='lines',
              x=df[['Date']],
              y=df[[i]],
              yaxis='y2',
              line=list(color=dfcolors[i],
                        width=3),
              showlegend=T,
              hovertext=paste0('<b>',i,': </b>',format(df[[i]],trim=T,big.mark=',')),
              hoverinfo='text')
}
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['Green Taxi']],
            showlegend=F,
            hovertext=paste0('<b>Total Trips: </b>',format(df[['Total Trips']],trim=T,big.mark=',')),
            hoverinfo='text')
for (i in c('For-Hire Vehicle','Yellow Taxi','Green Taxi')){
  p=p %>%
    add_trace(name=i,
              type='scatter',
              mode='none',
              x=df[['Date']],
              y=df[[i]],
              showlegend=T,
              stackgroup='one',
              groupnorm='',
              orientation='v',
              fill='tonexty',
              fillcolor=dfcolors[i],
              hovertext=paste0('<b>',i,': </b>',format(df[[i]],trim=T,big.mark=','),
                               ' (',format(round(df[[paste0(i,' Pct')]]*100,0),trim=T,nsmall=0),'%)'),
              hoverinfo='text')
}
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['Green Taxi']],
            showlegend=F,
            hovertext=paste0('<b>Month: </b>',format(df[['Date']],'%b %Y')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Taxi and For-Hire Vehicle Monthly Statistics</b>'),
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
         yaxis=list(title=list(text='<b>Number of Trips</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         yaxis2=list(title=list(text='<b>Number of Drivers / Vehicles</b>',
                                font=list(size=14)),
                     tickfont=list(size=12),
                     side='right',
                     overlaying='y',
                     rangemode='tozero',
                     fixedrange=T,
                     showgrid=F,
                     zeroline=F),
         hoverlabel=list(bgcolor='rgba(255,255,255,0.95)',
                         bordercolor='rgba(0,0,0,0.1)',
                         font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://www1.nyc.gov/site/tlc/about/aggregated-reports.page" target="blank">NYC TLC</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/tlc/TLC_Monthly.csv" target="blank">Download Chart Data</a>',
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
htmlwidgets::saveWidget(p,paste0(path,'tlc/TLC_Monthly.html'))




