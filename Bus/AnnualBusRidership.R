library(tidyverse)
library(plotly)
library(tibble)


Year <- c(2015, 2016, 2017, 2018, 2019, 2020)
Brooklyn <- c(202960156, 201470709, 190965796, 179169441, 175415701, 102269950)
Bronx <- c(174385554, 168831140, 156662777, 142690932, 134889542, 85610030)
Manhattan <- c(133326664, 128212381, 118715667, 116996185, 119868296, 57417780)
Queens <- c(223893375, 224625421, 218948349, 214805777, 212084034, 117556839)
Staten.Island <- c(38822492, 38404316, 37147936, 34993288, 34939479, 19418626)

df <- data.frame(Year, Brooklyn, Bronx, Manhattan, Queens, Staten.Island)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["Brooklyn"]], name = "Brooklyn", hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["Bronx"]], name = "Bronx", hovertemplate="%[y:,.0f") %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["Manhattan"]], name = "Manhattan", hovertemplate="%[y:,.0f") %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["Queens"]], name = "Queens", hovertemplate="%[y:,.0f") %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["Staten.Island"]], name = 'Staten Island', hovertemplate="%[y:,.0f") %>%
  layout(title = "Annual Bus Ridership", xaxis=list(title="Date"), yaxis=list(title="Ridership")) %>%
  layout(margin = list(b=160), annotations=list(x=1, y=-0.1, text= "Data Source: MTA", showarrow=F, xref="paper", yref="paper", xanchor="right", yanchor="top", xshift=0, yshift=0, font=list(size=12, color="grey"))) %>%
  config(displayModeBar = F)

p

path = "C:/Users/S_Sanich/Desktop/td-trends/Bus"

htmlwidgets::saveWidget(p,paste0(path,"AnnualBus.html"))
