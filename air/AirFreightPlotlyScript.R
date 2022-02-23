library(tidyverse)
library(plotly)
library(tibble)


Year <- c(2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)
Domestic_Freight <- c(1082384, 962975, 799745, 843903, 811377, 774842, 700393, 679116, 707657,
                      753926, 800548, 838227, 851209,889740)
International_Freight <- c(1554326, 1406782, 1141324, 1431313, 1407661, 1313381, 1308008, 1353169,
                           1352483, 1334961, 1444261, 1460898, 1342454, 988177)

df <- data.frame(Date, Domestic, International)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Year"]], 
            y=df[["Domestic_Freight"]], 
            name = "<b>Domestic Freight</b>",
            hovertemplate="%{y:,.0f}",
            color = "#729ece") %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Year"]], 
            y=df[["International_Freight"]], 
            name = "<b>International Freight</b>", 
            hovertemplate="%{y:,.0f}",
            color = "#ff9e4a") %>%
  layout(title = "<b>Annual Revenue Freight</b>", 
         xaxis=list(title="<b>Date</b>"), 
         yaxis=list(title="<b>Freight (in short tons)</b>")) %>%
  layout(margin = list(b=160), 
         annotations=list(x=1, y=-0.2, 
                          text= "Data Source: <a href='https://www.panynj.gov/airports/en/statistics-general-info.html' target='blank'>Port Authority of NY & NJ</a>", 
                          showarrow=F, 
                          xref="paper", yref="paper",
                          xanchor="right", yanchor="top", 
                          xshift=0, yshift=0, 
                          font=list(size=12, color="grey"))) %>%
  layout(xaxis=list(showgrid=FALSE)) %>%
  config(displayModeBar = F)

p


path = "C:/Users/S_Sanich/Desktop/td-trends/air"

htmlwidgets::saveWidget(p,paste0(path,"air_freight.html"))

