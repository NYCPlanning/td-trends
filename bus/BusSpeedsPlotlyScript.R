library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/BusSpeedAveragesbyBoroughUpdated.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

df=df %>%
  arrange(Month)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Month"]], y=df[["Brooklyn"]], 
            name = "Brooklyn", 
            color = "#ff9e4a",
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Month"]], y=df[["Bronx"]], 
            name = "Bronx", 
            color = "#729ece",
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Month"]], y=df[["Manhattan"]], 
            name = "Manhattan",
            color = "#67bf5c",
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Month"]], y=df[["Queens"]], 
            name = "Queens", 
            color = "#ad8bc9",
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Month"]], y=df[["Staten.Island"]], 
            name = 'Staten Island', 
            color = "#ed665d",
            hovertemplate="%{y:,.0f}") %>%
  layout(title = "<b>Bus Speeds in 2020-2021</b>", 
         xaxis=list(title="<b>Month/Year</b>"), yaxis=list(title="<b>Speed (mph)</b>")) %>%
  layout(margin = list(b=160), 
         annotations=list(x=1, y=-0.3, 
                          text= "Data Source: <a href='http://busdashboard.mta.info/' target='blank'>MTA</a> | <a href='https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/BusSpeedAveragesbyBoroughUpdated.csv' target='blank'>Download Chart Data</a>", 
                          showarrow=F, 
                          xref="paper", yref="paper", 
                          xanchor="right", yanchor="top",
                          xshift=0, yshift=0,
                          font=list(size=12, color="grey"))) %>%
  config(displayModeBar = F)

p

path = "C:/Users/S_Sanich/Desktop/td-trends/bus"

htmlwidgets::saveWidget(p,paste0(path,"bus_speeds.html"))
