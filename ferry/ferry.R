library(tidyverse)
library(plotly)

path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'

df=read.csv(paste0(path,'ferry/ferryop.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(paste0(yearmonth,'01'),'%Y%m%d')) %>%
  filter(Date>=as.Date('20150101','%Y%m%d'))

dfcolors=c('BillyBey'='#729ece',
           'Liberty Landing Ferry'='#ff9e4a',
           'NY Waterway'='#67bf5c',
           'NYC Ferry'='#ed665d',
           'New York Water Taxi'='#ad8bc9',
           'SeaStreak'='#a8786e',
           'Staten Island Ferry'='#ed97ca')

p=plot_ly()
for (i in list('BillyBey','Liberty Landing Ferry','NY Waterway','NYC Ferry','New York Water Taxi','SeaStreak','Staten Island Ferry')){
  p=p %>%
    add_trace(name=i,
              type='scatter',
              mode='lines',
              x=df[['Date']],
              y=df[[i]],
              line=list(color=dfcolors[i],
                        width=2),
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
                     l=80,
                     r=80,
                     t=120),
         xaxis=list(title=list(text='<b>Month</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    dtick='M6',
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Ridership</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='nonnegative',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='#444',
                    zerolinewidth=1),
         hoverlabel=list(font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p

# Remove camera and logo
# Annotation
# Title
# Stack Area
# Xaxis margin

htmlwidgets::saveWidget(p,paste0(path,'ferry/ferry.html'))




