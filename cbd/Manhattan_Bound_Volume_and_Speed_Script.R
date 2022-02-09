library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/cbd/CBDMN2019_2021.csv"

df = read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

colnames(df)

df[is.na(df)] = 0

df$Date=as.Date(df$Date, "%m/%d/%Y")

df=df %>%
  arrange(Date)

p=plot_ly()

p=p %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]],
            y=df[["Avg_CBDInbound"]],
            line = list(color = "#6dccda", width = 2),
            name = "CBD Inbound",
            hovertemplate = "%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode="lines",
            x=df[["Date"]],
            y=df[["Avg_MNInbound"]],
            line = list(color = "#cdcc5d", width = 2),
            name = "MN Inbound",
            hovertemplate = "%{y:,.0f}") %>%
  add_trace(type="scatter", 
            mode="lines",
            x=df[["Date"]],
            y=df[["Avg_ERB_In7a7p"]],
            line = list(color = "#a2a2a2", width = 2),
            name = "7AM-7PM ERB Inbound",
            hovertemplate ="%{y:,.0f}") %>%
  add_trace(type="scatter",
            mode = "lines",
            x=df[["Date"]],
            y=df[["Avg_MIM_Midtown_Speed"]],
            line=list(color="#ed97ca", width=2),
            name="MIM Midtown Speed*",
            yaxis = "y2",
            hovertemplate ="%{y:,.0f}") %>%
  layout(yaxis2 = list(range = c(as.Date("2020-03-12"), as.Date("2021-12-03")))) %>%
  layout(yaxis2 = list(overlaying = "y", side="right")) %>%
  layout(title = "<b>Manhattan-Bound Traffic Volume and Speed (Seven Day Average)</b>",
         xaxis = list(title="<b>Date</b>"),
         yaxis = list(title="<b>Total Vehicles</b>"),
         yaxis2 = list(title="<b>Miles Per Hour</b>")) %>%
  config(displayModeBar=F) %>%
  layout(annotations=list(text='Data Source: NYC DOT', 
                          font=list(size=11),
                          showarrow=F,
                          x=1,
                          xanchor='right',
                          xref='paper',
                          y=-0.2,
                          yanchor='top',
                          yref='paper')) %>%
  layout(annotations=list(text="*Note: As the Midtown speed in the pre-COVID period is not available, Taxi speed for that area and period is used instead",
                          font=list(size=11),
                          showarrow=F,
                          x=1,
                          xanchor='right',
                          xref='paper',
                          y=-0.3,
                          yanchor='top',
                          yref='paper')) %>%
  layout(margin = list(b=160)) %>%
  config(displayModeBar=F)


p

path = "C:/Users/S_Sanich/Desktop/td-trends/cbd"

htmlwidgets::saveWidget(p,paste0(path,"manhattan-bound.html"))



