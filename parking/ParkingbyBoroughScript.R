library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Off-Street_Parking_By_Borough.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

df$Date=as.Date(df$Year,"%m/%d/%Y")

df=df %>%
  arrange("Date")
  

p=plot_ly()

p=p %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]], y=df[["Bronx"]],
            name="Bronx",
            color = "#729ece",
            hovertemplate='%{y:,.0f}') %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]], y=df[["Brooklyn"]],
            name="Brooklyn",
            color="#ff9e4a",
            hovertemplate='%{y:,.0f}') %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]], y=df[["Manhattan"]],
            name="Manhattan",
            color = "#67bf5c",
            hovertemplate='%{y:,.0f}') %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]], y=df[["Queens"]],
            name="Queens",
            color="#ad8bc9",
            hovertemplate='%{y:,.0f}') %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]], y=df[["Staten.Island"]],
            name="Staten Island",
            color = "#ed665d",
            hovertemplate='%{y:,.0f}') %>%
  layout(title = "<b>NYC DCA Public Parking Spaces 2005-2021, by Borough</b>", 
         xaxis=list(title="<b>Year</b>"), yaxis=list(title="<b>Parking Capacity</b>")) %>%
  layout(margin = list(b=160),
         annotations=list(x=1, y=-0.2,
                          text= "Data Source: DCA | <a href='https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Off-Street_Parking_By_Borough.csv' target='blank'>Download Chart Data</a>", 
                          showarrow=F,
                          xref="paper", yref="paper",
                          xanchor="right", yanchor="top",
                          xshift=0, yshift=0,
                          font=list(size=12, color="grey"))) %>%
  config(displayModeBar = F)



p

path = "C:/Users/S_Sanich/Desktop/td-trends/parking"

htmlwidgets::saveWidget(p,paste0(path,"Borough_Parking.html"))

