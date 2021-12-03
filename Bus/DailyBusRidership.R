library(tidyverse)
library(plotly)

url="https://new.mta.info/document/20441"

df=read.csv(url,stringsAsFactors=F)

df=df %>%
  mutate(Date=as.Date(Date, "%m/%d/%Y")) %>%
  arrange(Date)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", mode="lines", x=df[["Date"]], y=df[["Buses..Total.Estimated.Ridership"]], hovertemplate="%{y:,.0f}") %>%
  layout(title = "Daily Bus Ridership During COVID-19", xaxis=list(title="Date"), yaxis=list(title="Ridership")) %>%
  layout(showlegend=FALSE)%>%
  layout(margin = list(b=160), annotations=list(x=1, y=-0.1, text= "Data Source: MTA", showarrow=F, xref="paper", yref="paper", xanchor="right", yanchor="top", xshift=0, yshift=0, font=list(size=12, color="grey"))) %>%
  config(displayModeBar = F)

p

path = "C:/Users/S_Sanich/Desktop/td-trends/Bus"

htmlwidgets::saveWidget(p,paste0(path,"DailyBus.html"))
