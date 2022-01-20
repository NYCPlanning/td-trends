library(tidyverse)
library(plotly)

url= "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/subway/1904-2020Ridership.csv"

df=read.csv(url, stringsAsFactors = F)

p=plot_ly()

p=p %>%
  add_trace(type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Ridership']],
            hovertemplate='%{y:,.0f}',
            color="#6dccda") %>%
  layout(title="Annual Subway Ridership", axis=list(title="Date", showgrid=F), yaxis=list(title="Ridership", showgrid=F)) %>%
  layout(margin = list(b=160), annotations=list(x=1, y=-0.2, text= "Data Source: MTA", showarrow=F, xref="paper", yref="paper", xanchor="right", yanchor="top", xshift=0, yshift=0, font=list(size=12, color="grey"))) %>%
  layout(showlegend=FALSE) %>%
  config(displayModeBar = F)


p

path = "C:/Users/S_Sanich/Desktop/td-trends/subway"

htmlwidgets::saveWidget(p,paste0(path,"annualsubway.html"))


