library(tidyverse)
library(plotly)
library(tibble)

Month <- c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep")
EWR <- c(907722, 866573,1348319,1714836,1864551,1982169,2205406,2216927, 1913598)
JFK <- c(563853, 571434, 721380, 1121056, 1362198, 1812488, 2069124, 2020825, 1637644)
LGA <- c(496152, 428684, 685314, 898135, 1093240, 1186959, 1658154, 1468457, 1408362)

df <- data.frame(Month, EWR, JFK, LGA)

fig <- plot_ly(df, 
               x= ~Month, y= ~EWR, 
               type = "bar", 
               name = "EWR", 
               marker = list(color = "#6dccda"),
               hovertemplate = paste('%{y:,.0f}'),
               texttemplate = '%{y:.2s}', textposition = 'outside')
fig <- fig %>% add_trace(y = ~JFK, 
                         name = "JFK", 
                         marker = list(color="#cdcc5d"),
                         hovertemplate = paste('%{y:,.0f}'),
                         texttemplate = '%{y:.2s}', textposition = 'outside')
fig <- fig %>% add_trace(y = ~LGA, 
                         name = "LGA", 
                         marker = list(color="#a2a2a2"),
                         hovertemplate = paste('%{y:,.0f}'),
                         texttemplate = '%{y:.2s}', textposition = 'outside')
fig <- fig %>% layout(xaxis = list(title = "<b>Month", tickangle = -45))
fig <- fig %>% layout(yaxis = list(title = "<b>Number of Passengers"))
fig <- fig %>% layout(title = "<b>Monthly Air Passenger Traffic in 2021")
fig <- fig %>% config(displayModeBar = F)
fig <- fig %>% layout(margin = list(b=160), 
                      annotations=list(x=1, y=-0.2, 
                                       text= 'Data Source: <a href="https://www.panynj.gov/airports/en/statistics-general-info.html", target="blank">Port Authority of NY and NJ</a>', 
                                       showarrow=F, 
                                       xref="paper", yref="paper",
                                       xanchor="right", yanchor="top", 
                                       xshift=0, yshift=0, 
                                       font=list(size=12, color="grey")))



fig


path = "C:/Users/S_Sanich/Desktop/td-trends/air"

htmlwidgets::saveWidget(p,paste0(path,"monthly_air_passenger_traffic.html"))                  
