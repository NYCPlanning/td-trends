library(tidyverse)
library(plotly)

url="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/MTA_Bus_and_Subway_Ridership_Averages.csv"

df=read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors=F)

colnames(df)

df=df %>%
  mutate(Date=as.Date(Date, "%m/%d/%Y")) %>%
  arrange(Date)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Date"]], 
            y=df[["Buses..Average.Estimated.Ridership"]], 
            line = list(color = "#6dccda", width = 2),
            hovertemplate="%{y:,.0f}") %>%
  layout(title = "Daily Bus Ridership", 
         xaxis=list(title="Date"), 
         yaxis=list(title="Ridership")) %>%
  layout(showlegend=FALSE)%>%
  layout(margin = list(b=160), 
         annotations=list(x=1, y=-0.2, 
                          text= 'Data Source: <a href="https://new.mta.info/coronavirus/ridership", target="blank">MTA</a>', 
                          showarrow=F, 
                          xref="paper", yref="paper", 
                          xanchor="right", yanchor="top", 
                          xshift=0, yshift=0, 
                          font=list(size=12, color="grey"))) %>%
  config(displayModeBar = F)

p
