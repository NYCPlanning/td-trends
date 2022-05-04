library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/M14BusSpeedsPeak.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)
            
df=df %>%
  arrange(Month)
            
p=plot_ly()
            
p=p %>%
  add_trace(type="scatter",
            mode= "lines+markers",
            x=df[["Month"]],
            y=df[["average_speed"]],
            color = "#ff9e4a",
            hoverinto = "text")
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b> 14th Street Busway Speeds</b>'),
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
         xaxis=list(title=list(text='<b>Month</b>',
                               font=list(size=14)),
                   showgrid=F),
         yaxis=list(title=list(text='<b>Speed (mph)</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
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
  add_annotations(text='Data Source: <a href="http://busdashboard.mta.info/" target="blank">MTA</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/M14BusSpeedsPeak.csv" target="blank">Download Chart Data</a>',
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
         displaylogo=F,
         modeBarButtonsToRemove=c('select','lasso2d'))
            
p
            
path = "C:/Users/S_Sanich/Desktop/td-trends/bus"

htmlwidgets::saveWidget(p,paste0(path,"M14buswayspeedschart.html"))

            