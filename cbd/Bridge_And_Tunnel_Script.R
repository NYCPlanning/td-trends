library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/cbd/Bridge_Tunnel_Crossings.csv"

df = read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

colnames(df)

df$Year=as.Date(df$Year, "%m/%d/%Y")

df=df %>%
  arrange(Year)

p=plot_ly()

p=p %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Year"]],
            y=df[["George_Washington_Bridge"]],
            line = list(color = "#6dccda", width = 4),
name = "George Washington Bridge",
hovertemplate = "%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Year"]],
            y=df[["Lincoln_Tunnel"]],
            line = list(color = "#cdcc5d", width = 4),
            name = "Lincoln Tunnel",
            hovertemplate = "%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines",
            x=df[["Year"]],
            y=df[["Holland_Tunnel"]],
            line = list(color = "#a2a2a2", width = 4),
            name = "7AM-7PM ERB Inbound",
            hovertemplate ="%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode = "lines",
            x=df[["Year"]],
            y=df[["Goethals_Bridge"]],
            line=list(color="#ed97ca", width=4),
            name="Goethals Bridge",
            hovertemplate ="%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode = "lines",
            x=df[["Year"]],
            y=df[["Outerbridge_Crossing"]],
            line=list(color="#a8786e", width=4),
            name="Outerbridge Crossing",
            hovertemplate ="%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode = "lines",
            x=df[["Year"]],
            y=df[["Bayonne_Bridge"]],
            line=list(color="#ad8bc9", width=4),
            name="Bayonne Bridge",
            hovertemplate ="%{y:,.0f}") %>%
  layout(title = "<b>Bridge and Tunnel Crossings</b>",
         xaxis = list(title="<b>Year</b>"),
         yaxis = list(title="<b>Number of Crossings</b>")) %>%
  config(displayModeBar=F) %>%
  layout(annotations=list(text='Data Source: <a href ="https://www.panynj.gov/bridges-tunnels/en/traffic---volume-information---b-t.html" target = "blank">The Port Authority of NY & NJ</a>', 
                          font=list(size=11),
                          showarrow=F,
                          x=1,
                          xanchor='right',
                          xref='paper',
                          y=-0.2,
                          yanchor='top',
                          yref='paper')) %>%
  
  layout(margin = list(b=160)) %>%
  config(displayModeBar=F)


p

path = "C:/Users/S_Sanich/Desktop/td-trends/cbd"

htmlwidgets::saveWidget(p,paste0(path,"bridge_and_tunnel_crossing.html"))


