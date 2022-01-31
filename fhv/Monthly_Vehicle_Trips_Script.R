library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/fhv/TLC_Monthly_Ridership_EstimatedTotals.csv"

df = read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

df=df %>%
  arrange(Time)

p=plot_ly()

p=p %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Time"]],
            y=df[["FHV"]],
            line = list(color = "#729ece", width = 2),
            name = "FHV",
            hovertemplate = "%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Time"]],
            y=df[["Green"]],
            line = list(color = "#67bf5c", width = 2),
            name = "Green",
            hovertemplate = "%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines",
            x=df[["Time"]],
            y=df[["Yellow"]],
            line = list(color = "#cdcc5d", width = 2),
            name = "Yellow",
            hovertemplate ="%{y:,.0f}") %>%
  layout(title = "NYCTLC Monthly Vehicle Trips, by Vehicle License Type, 2015-2021",
         xaxis = list(title="Month/Year"),
         yaxis = list(title="Number of Trips")) %>%
  config(displayModeBar=F) %>%
  layout(annotations=list(text='Data Source: <a href="https://www1.nyc.gov/site/tlc/about/aggregated-reports.page", target="blank">NYCTLC</a>', 
                          font=list(size=11),
                          showarrow=F,
                          x=1,
                          xanchor='right',
                          xref='paper',
                          y=-0.2,
                          yanchor='top',
                          yref='paper')) %>%
  layout(annotations=list(text='Note: Trips do not equal ridership because they may be pooled', 
                          font=list(size=11),
                          showarrow=F,
                          x=1,
                          xanchor='right',
                          xref='paper',
                          y=-0.3,
                          yanchor='top',
                          yref='paper')) %>%
  layout(margin = list(b=160)) %>%
  config(displayModeBar=F)

p


path = "C:/Users/S_Sanich/Desktop/td-trends/fhv"

htmlwidgets::saveWidget(p,paste0(path,"monthly.html"))
