library(tidyverse)
library(plotly)



# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=read.csv(paste0(path,'parking/countytime.csv'),stringsAsFactors=F,check.names=F)

dfcolors=c('Bronx'='rgba(114,158,206,0.8)',
           'Brooklyn'='rgba(255,158,74,0.8)',
           'Manhattan'='rgba(103,191,92,0.8)',
           'Queens'='rgba(237,102,93,0.8)',
           'Staten Island'='rgba(173,139,201,0.8)')

p=plot_ly()
p=p %>%
  add_trace(type="scatter",
            mode="none",
            x=df[["time"]], 
            y=df[["Manhattan"]],
            showlegend=F,
            hovertext=paste0('<b>Time: </b>',df[['time']]),
            hoverinfo='text')
for (i in c('Bronx','Brooklyn','Manhattan','Queens','Staten Island')){
  p=p %>%
    add_trace(name=i,
              mode="lines",
              type='scatter',
              x=df[['time']],
              y=df[[i]],
              line=list(color=dfcolors[i],
                        width=3),
              showlegend=T,
              hovertext=paste0('<b>',i,': </b>',format(df[[i]],trim=T,big.mark=','),
                               ' (',format(round(df[[paste0(i,' Pct')]]*100,0),trim=T,nsmall=0),'%)'),
              hoverinfo='text')
}
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['time']],
            y=df[['Manhattan']],
            showlegend=F,
            hovertext=paste0('<b>Total: </b>',format(df[['Allowed']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Free / Metered Parking Spaces</b>'),
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
         margin=list(b=140,
                     l=80,
                     r=40,
                     t=160),
         xaxis=list(title=list(text='<b>Time</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    categoryarray=df[['time']],
                    range=c(-1,nrow(df)),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Spaces</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         barmode='stack',
         hoverlabel=list(bgcolor='rgba(255,255,255,0.95)',
                         bordercolor='rgba(0,0,0,0.1)',
                         font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://data.cityofnewyork.us/Transportation/Parking-Regulation-Locations-and-Signs/xswq-wnv9" target="blank">NYC DOT</a>; <a href="https://github.com/NYCPlanning/td-parking/blob/master/onstparking/ONSTPARKING.pdf" target="blank">NYC DCP</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/countytime.csv" target="blank">Download Chart Data</a>',
                  font=list(size=14),
                  showarrow=F,
                  x=1,
                  xanchor='right',
                  xref='paper',
                  y=0,
                  yanchor='top',
                  yref='paper',
                  yshift=-100)
p=p %>%
  config(displayModeBar=T,
         displaylogo=F)
p
htmlwidgets::saveWidget(p,paste0(path,"parking/countytime.html"))
  
 