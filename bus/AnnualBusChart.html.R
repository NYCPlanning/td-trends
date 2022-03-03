library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'bus/BusRidership2008-2020.csv'),stringsAsFactors=F,check.names=F)

dfcolors=c('Bronx'='rgba(114,158,206,0.8)',
           'Brooklyn'='rgba(255,158,74,0.8)',
           'Manhattan'='rgba(103,191,92,0.8)',
           'Queens'='rgba(237,102,93,0.8)',
           'Staten Island'='rgba(173,139,201,0.8)')

p=plot_ly()
for (i in c('Bronx','Brooklyn','Manhattan','Queens','Staten Island')){
  p=p %>%
    add_trace(name=i,
              type='scatter',
              mode='lines+markers',
              x=df[['Year']],
              y=df[[i]],
              line=list(color=dfcolors[i],
                        width=2),
              showlegend=T,
              hovertemplate='%{y:,.0f}')
}
p

p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Annual Bus Ridership</b>'),
                    font=list(size=20),
                    x=0.5,
                    xanchor='center',
                    y=0.95,
                    yanchor='top'),
         margin=list(b=120,
                     l=80,
                     r=40,
                     t=120),
         xaxis=list(title=list(text='<b>Year</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    range=c(-1,nrow(df['Year'])),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Ridership</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='nonnegative',
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
  add_annotations(text='2.05 billion<br>in 1929-1930',
                  font=list(size=10),
                  showarrow=F,
                  x='1929-30',
                  xanchor='center',
                  xref='x',
                  y=2100000000,
                  yanchor='bottom',
                  yref='y')

p=p %>% 
  add_annotations(text='2.07 billion<br>in 1946',
                  font=list(size=10),
                  showarrow=F,
                  x=41,
                  xanchor='center',
                  xref='x',
                  y=2100000000,
                  yanchor='bottom',
                  yref='y')

p=p %>% 
  add_annotations(text='1.76 billion<br>in 2015',
                  font=list(size=10),
                  showarrow=F,
                  x=110,
                  xanchor='center',
                  xref='x',
                  y=1800000000,
                  yanchor='bottom',
                  yref='y')

p=p %>% 
  add_annotations(text='640 million<br>in 2020',
                  font=list(size=10),
                  showarrow=F,
                  x=115,
                  xanchor='center',
                  xref='x',
                  y=620000000,
                  yanchor='top',
                  yref='y')

p=p %>% 
  add_annotations(text='*Reported by Fiscal Year Before 1940',
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
  add_annotations(text='Data Source: <a href="https://new.mta.info/agency/new-york-city-transit/subway-bus-ridership-2020" target="blank">MTA</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/subway/SubwayRidership1904-2020.csv" target="blank">Download Chart Data</a>',
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
htmlwidgets::saveWidget(p,paste0(path,'subway/AnnualSubwayChart.html'))





