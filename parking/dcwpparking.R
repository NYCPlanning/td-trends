library(tidyverse)
library(plotly)



path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
# path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'



df=read.csv(paste0(path,'parking/dcwpparking.csv'),stringsAsFactors=F,check.names=F)

dfcolors=c('Bronx'='rgba(114,158,206,0.8)',
           'Brooklyn'='rgba(255,158,74,0.8)',
           'Manhattan'='rgba(103,191,92,0.8)',
           'Queens'='rgba(237,102,93,0.8)',
           'Staten Island'='rgba(173,139,201,0.8)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Year']],
            y=df[['Staten Island']],
            showlegend=F,
            hovertext=paste0('<b>Total: </b>',format(df[['Total']],trim=T,big.mark=',')),
            hoverinfo='text')
for (i in c('Staten Island','Queens','Manhattan','Brooklyn','Bronx')){
p=p %>%
  add_trace(name=i,
            type='bar',
            x=df[['Year']],
            y=df[[i]],
            marker=list(color=dfcolors[i]),
            width=0.5,
            showlegend=T,
            hovertext=paste0('<b>',i,': </b>',format(df[[i]],trim=T,big.mark=','),
                             ' (',format(round(df[[paste0(i,' Pct')]]*100,0),trim=T,nsmall=0),'%)'),
            hoverinfo='text')
}
p=p %>%
  add_trace(type="scatter",
            mode="none",
            x=df[["Year"]], 
            y=df[["Staten Island"]],
            showlegend=F,
            hovertext=paste0('<b>Year: </b>',df[['Year']]),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>DCWP Public Parking Spaces</b>'),
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
         xaxis=list(title=list(text='<b>Year</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    dtick='M12',
                    range=c(min(df[['Year']])-0.5,max(df[['Year']])+0.5),
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
         hoverlabel=list(font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://data.cityofnewyork.us/Business/Legally-Operating-Businesses/w7w3-xahh" target="blank">NYC DCWP</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/dcwpparking.csv" target="blank">Download Chart Data</a>',
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

htmlwidgets::saveWidget(p,paste0(path,"parking/dcwpparking.html"))
  
 