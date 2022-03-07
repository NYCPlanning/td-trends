library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Two_Year_Citywide_Average.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

df=df %>%
  arrange("Year")

fig <- plot_ly(df, x= ~Year,
               y= ~Manhattan, 
               type = "bar", 
               name = "Manhattan", 
               marker = list(showticklabels=TRUE,
                             color = "rgba(103,191,92,0.8)"))
fig <- fig %>% add_trace(y = ~Brooklyn,
                         name = "Brooklyn",
                         marker = list(color= "rgba(255,158,74,0.8)"))
fig <- fig %>% add_trace(y=~Queens,
                         name="Queens",
                         marker = list(color = "rgba(237,102,93,0.8)"))
fig <- fig %>% add_trace(y=~Staten.Island,
                         name="Staten Island",
                         marker = list(color = "rgba(173,139,201,0.8)"))
fig <- fig %>% add_trace(y=~Bronx,
                         name="Bronx",
                         marker = list(color = "rgba(114,158,206,0.8)"))
fig <- fig %>% layout(yaxis = list(title = "<b>Parking Capacity</b>"), barmode = "stack")
fig <- fig %>% layout(xaxis = list(title = "<b>Year</b>"))
fig <- fig %>% layout(title = "<b>NYC DCA Public Parking Spaces, 2005-2021, by Borough</b>")
fig <- fig %>% config(displayModeBar = F)
fig <- fig %>% layout(margin = list(b=160), 
                      annotations=list(x=1, y=-0.2, 
                                       text= "Data Source: NYC DCA | <a href='https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Two_Year_Citywide_Average.csv' target='blank'>Download Chart Data</a>", 
                                       showarrow=F, 
                                       xref="paper", yref="paper",
                                       xanchor="right", yanchor="top", 
                                       xshift=0, yshift=0, 
                                       font=list(size=12, 
                                                 color="grey")))

fig

path = "C:/Users/S_Sanich/Desktop/td-trends/parking"

htmlwidgets::saveWidget(p,paste0(path,"Borough_Parking_Bar_Chart.html"))



