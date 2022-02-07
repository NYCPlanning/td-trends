library(tidyverse)
library(plotly)
library(tibble)

Year <- c(2015, 2016, 2017, 2018, 2019, 2020, 2021)
EWR_Domestic <- c(25691410, 28218424, 30330568, 31730735, 32004140, 12121093, 15020101)
EWR_International <- c(11805317, 12344869, 12888553, 14128785, 14332312, 3771799, 4385476)
JFK_Domestic <- c(26806854, 27324138, 26961081, 25117337, 28233791, 8267666, 11880002)
JFK_International <- c(30077876, 31779334, 32527901, 33518898, 34317281, 8362976, 8719894)
LGA_Domestic <- c(26684923, 27996855, 27474292, 27857697, 28875041, 7853368, 9323457)
LGA_International <- c(1752745, 1790006, 2087936, 2224430, 2209853, 391824, 112094)

df <- data.frame(Year, EWR_Domestic, EWR_International, JFK_Domestic, JFK_International,
                 LGA_Domestic, LGA_International)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", mode="lines", 
            x=df[["Year"]], y=df[["EWR_Domestic"]], 
            line = list(color = "#6dccda", width = 2),
            name = "EWR Domestic", 
            hovertemplate="%{y:,.0f}") %>% 
  add_trace(type="scatter", mode="lines", 
            line = list(color = "#6dccda", width = 2, dash="dot"),
            x=df[["Year"]], y=df[["EWR_International"]], 
            name = "EWR International", 
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", mode="lines", 
            line = list(color = "#cdcc5d", width = 2),
            x=df[["Year"]], y=df[["JFK_Domestic"]], 
            name = "JFK Domestic", 
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", mode="lines", 
            line = list(color = "#cdcc5d", width = 2, dash = "dot"),
            x=df[["Year"]], y=df[["JFK_International"]], 
            name = "JFK International", 
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", mode="lines", 
            line = list(color = "#a2a2a2", width = 2),
            x=df[["Year"]], y=df[["LGA_Domestic"]], 
            name = "LGA Domestic", 
            hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", mode="lines", 
            line = list(color = "#a2a2a2", width = 2, dash = "dot"),
            x=df[["Year"]], y=df[["LGA_International"]], 
            name = "LGA International", 
            hovertemplate="%{y:,.0f}") %>%
  layout(title = "<b>Annual Air Passenger Traffic Per Airport</b>", 
         xaxis=list(title="<b>Date</b>"), 
         yaxis=list(title="<b>Number of Passengers</b>")) %>%
  layout(margin = list(b=160), 
         annotations=list(x=1, y=-0.2, 
                          text= "Data Source: <a href='https://www.panynj.gov/airports/en/statistics-general-info.html' target='blank'> Port Authority of NY and NJ </a>", 
                          showarrow=F, 
                          xref="paper", yref="paper", 
                          xanchor= "right", yanchor = "top",
                          xshift=0, yshift=0, font=list(size=12, color="grey"))) %>%
  layout(xaxis=list(showgrid=FALSE)) %>%
  config(displayModeBar=F)

p

path = "C:/Users/S_Sanich/Desktop/td-trends/air"

htmlwidgets::saveWidget(p,paste0(path,"annualair.html"))
