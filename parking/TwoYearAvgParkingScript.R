library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Two_Year_Citywide_Average.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)


df=df %>%
  arrange("Year")

fig <- plot_ly(df, x=~Year, y=~Capacity,
               type="bar",
               marker=list(color="#1b9e77",
                           showticklabels=TRUE),
               text=~Capacity, textposition = "auto")
fig <- fig %>% layout(yaxis=list(title="<b>Parking Capacity<b>"))
fig <- fig %>% layout(xaxis=list(title="<b>Year<b>"))
fig <- fig %>% layout(title="<b>NYC DCA Public Parking Spaces in NYC, 1998-2021<b>")
fig <- fig %>% config(displayModeBar = F)
fig <- fig %>% layout(margin=list(b=160),
                      annotations=list(x=1, y=-0.2,
                                       text = 'Data Source: NYC DCA | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/parking/Off-Street_Parking_By_Borough.csv" target="blank">Download Chart Data</a>',
                                       showarrow=F, 
                                       xref="paper", yref="paper", 
                                       xanchor="right", yanchor="top",
                                       xshift=0, yshift=0,
                                       font=list(size=12, color="grey")))



fig

path = "C:/Users/S_Sanich/Desktop/td-trends/parking"

htmlwidgets::saveWidget(fig,paste0(path,"twoyr_avg_parking.html"))
