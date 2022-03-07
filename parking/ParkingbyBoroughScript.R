library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Two_Year_Citywide_Average.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F, check.names=F)

df=df %>%
  arrange("Year")

dfcolors=c('Bronx'='rgba(114,158,206,0.8)',
           'Brooklyn'='rgba(255,158,74,0.8)',
           'Manhattan'='rgba(103,191,92,0.8)',
           'Queens'='rgba(237,102,93,0.8)',
           'Staten Island'='rgba(173,139,201,0.8)')

p=plot_ly()

p=p %>%
  add_trace(type="scatter",
            mode="none",
            x=df[["Year"]], 
            y=df[["Bronx"]],
            showlegend=F,
            hovertext=paste0('<b>Year: </b>',df[['Year']]),
            hoverinfo='text')
for (i in c('Bronx','Brooklyn','Manhattan','Queens','Staten Island')){
p=p %>%
  add_trace(name=i,
            type='scatter',
            mode='lines+markers',
            x=df[['Year']],
            y=df[[i]],
            line=list(color=dfcolors[i],
                      width=2),
            marker=list(color=dfcolors[i],
                        size=6),
            showlegend=T,
            hovertext=paste0('<b>',i,': </b>',format(df[[i]],trim=T,big.mark=','),
                             ' (',format(round(df[[paste0(i,' Pct')]]*100,0),trim=T,nsmall=0),'%)'),
            hoverinfo='text')
}

p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Year']],
            y=df[['Staten.Island']],
            showlegend=F,
            hovertext=paste0('<b>Total: </b>',format(df[['Total']],trim=T,big.mark=',')),
            hoverinfo='text')

p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>NYC DCA Public Parking Spaces 2005-2021, by Borough</b>'),
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
                    range=c(min(df[['Year']])-0.5,max(df[['Year']])+0.5),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Parking Capacity</b>',
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
  add_annotations(text='Data Source: DCA | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Two_Year_Citywide_Average.csv" target="blank">Download Chart Data</a>',
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

path = "C:/Users/S_Sanich/Desktop/td-trends/parking"

htmlwidgets::saveWidget(p,paste0(path,"Borough_Parking.html"))
  
 