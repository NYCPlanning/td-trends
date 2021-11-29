library(tidyverse)
library(plotly)

path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'

df=read.csv(paste0(path,'ferry/ferryop.csv'),stringsAsFactors=F)
df=df %>%
  mutate(Date=as.Date(paste0(yearmonth,'01'),'%Y%m%d'))





dfcolors=c('NYC.Ferry'='#729ece',
           'Staten.Island.Ferry'='#ff9e4a')
p=plot_ly()
for (i in list('NYC.Ferry','Staten.Island.Ferry')){
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
              hovertemplate='%{y:,.0f}',
              xhoverformat='<b>%Y-%m</b>')
}
p=p%>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>test</b>'),
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
                     t=120),
         xaxis=list(title=list(text='<b>Year</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    dtick='M6',
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='Ridership',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='nonnegative',
                    fixedrange=T,
                    showgrid=T),
         hoverlabel=list(font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p
htmlwidgets::saveWidget(p,paste0(path,'ferry/ferry.html'))

library(htmlwidgets)
saveWidget(p, paste0(path,'ferry/ferry.html'),selfcontained = T)




