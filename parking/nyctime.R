library(tidyverse)
library(plotly)



# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=read.csv(paste0(path,'parking/countytime.csv'),stringsAsFactors=F,check.names=F)

dfcolors=c('Free'='rgba(168,120,110,0.6)',
           'Metered'='rgba(109,204,218,0.6)',
           'No'='rgba(205,204,93,0.6)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['time']],
            y=df[['Metered']],
            showlegend=F,
            hovertext=paste0('<b>Total: </b>',format(df[['Total']],trim=T,big.mark=',')),
            hoverinfo='text')
for (i in c('Free','Metered','No')){
  p=p %>%
    add_trace(name=paste0(i,' Parking'),
              mode="none",
              type='scatter',
              x=df[['time']],
              y=df[[i]],
              showlegend=T,
              stackgroup='one',
              groupnorm='',
              orientation='v',
              fill='tonexty',
              fillcolor=dfcolors[i],
              showlegend=T,
              hovertext=paste0('<b>',i,' Parking: </b>',format(df[[i]],trim=T,big.mark=','),
                               ' (',format(round(df[[paste0(i,' Pct')]]*100,0),trim=T,nsmall=0),'%)'),
              hoverinfo='text')
}
p=p %>%
  add_trace(type="scatter",
            mode="none",
            x=df[["time"]], 
            y=df[["Metered"]],
            showlegend=F,
            hovertext=paste0('<b>Time: </b>',df[['time']]),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>NYC Total On-Street Parking Spaces</b>'),
                    font=list(size=20),
                    x=0.5,
                    xanchor='center',
                    y=0.95,
                    yanchor='top'),
         legend=list(orientation='v',
                     title=list(text=''),
                     font=list(size=14),
                     x=1,
                     xanchor='left',
                     y=0.5,
                     yanchor='middle'),
         margin=list(b=140,
                     l=80,
                     r=40,
                     t=60),
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
         hoverlabel=list(font=list(size=14)),
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
  config(displayModeBar=F)
p

htmlwidgets::saveWidget(p,paste0(path,"parking/nyctime.html"))
  
 