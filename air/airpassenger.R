library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'air/airpassenger.csv'),stringsAsFactors=F,check.names=F)

dfcolors=c('JFK'='rgba(237,102,93,0.8)',
           'EWR'='rgba(114,158,206,0.8)',
           'LGA'='rgba(103,191,92,0.8)')

p=plot_ly()
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Year']],
            y=df[['LGA Int.']],
            showlegend=F,
            hovertext=paste0('<b>Year: </b>',df[['Year']]),
            hoverinfo='text')
for (i in c('JFK','EWR','LGA')){
  p=p %>%
    add_trace(name=paste0(i,' Dom.'),
              type='scatter',
              mode='lines',
              x=df[['Year']],
              y=df[[paste0(i,' Dom.')]],
              line=list(color=dfcolors[i],
                        width=3),
              showlegend=T,
              hovertext=paste0('<b>',i,' Domestic: </b>',format(df[[paste0(i,' Dom.')]],trim=T,big.mark=','),
                               ' (',format(round(df[[paste0(i,' Dom. Pct')]]*100,0),trim=T,nsmall=0),'%)'),
              hoverinfo='text')
  p=p %>%
    add_trace(name=paste0(i,' Int.'),
              type='scatter',
              mode='lines',
              x=df[['Year']],
              y=df[[paste0(i,' Int.')]],
              line=list(color=dfcolors[i],
                        width=3,
                        dash='dot'),
              showlegend=T,
              hovertext=paste0('<b>',i,' International: </b>',format(df[[paste0(i,' Int.')]],trim=T,big.mark=','),
                               ' (',format(round(df[[paste0(i,' Int. Pct')]]*100,0),trim=T,nsmall=0),'%)'),
              hoverinfo='text')
}
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Year']],
            y=df[['LGA Int.']],
            showlegend=F,
            hovertext=paste0('<b>Total Passengers: </b>',format(df[['Total']],trim=T,big.mark=',')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Airport Commercial Passenger Traffic</b>'),
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
                     t=160),
         xaxis=list(title=list(text='<b>Year</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    range=c(min(df[['Year']])-0.5,max(df[['Year']])+0.5),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Passengers</b>',
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
  add_annotations(text='Data Source: <a href="https://www.panynj.gov/airports/en/statistics-general-info.html" target="blank">PANYNJ</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/air/airpassenger.csv" target="blank">Download Chart Data</a>',
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
htmlwidgets::saveWidget(p,paste0(path,'air/airpassenger.html'))





