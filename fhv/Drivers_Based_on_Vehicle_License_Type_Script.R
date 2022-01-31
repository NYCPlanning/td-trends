library(tidyverse)
library(plotly)
library(tibble)

url = "https://raw.githubusercontent.com/NYCPlanning/td-trends/main/fhv/Monthly_Unique_Drivers.csv"

df = read.csv(url, fileEncoding = 'UTF-8-BOM', stringsAsFactors = F)

colnames(df)

df$Date=as.Date(df$Month.Year, "%Y")

df=df %>%
  arrange("Date")

fig <- plot_ly(df, 
               x=~Date, y=~FHV...Black.Car,
               type = "bar",
               name = "FHV (Black Car)",
               marker=list(color = "#6dccda"),
               hovertemplate = "Black Car: %{y}")

fig <- fig %>% add_trace(y=~FHV...High.Volume, 
                         name = "FHV (High Volume)",    
                         marker = list(color = "#729ece"),
                         hovertemplate = "High Volume: %{y}")

fig <- fig %>% add_trace(y=~FHV...Livery,
                         name = "FHV (Livery)",
                         marker = list(color = "#a2a2a2"),
                         hovertemplate = "Livery: %{y}")

fig <- fig %>% add_trace(y=~FHV...Lux.Limo,
                         name = "FHV (Luxury Limo)",
                         marker = list(color = "#ed97ca"),
                         hovertemplate = "Luxury Limo: %{y}")

fig <- fig %>% add_trace(y=~Green, 
                         name = "Green",
                         marker = list(color = "#67bf5c"),
                         hovertemplate = "Green: %{y}")

fig <- fig %>% add_trace(y =~Yellow,
                         name = "Yellow",
                         marker = list(color = "#cdcc5d"),
                         hovertemplate = "Yellow: %{y}")

fig <- fig %>% layout(yaxis = list(title="Number of Drivers"), barmode = "stack")

fig <- fig %>% layout(xaxis = list(title = "Year"))

fig  <- fig %>% layout(title = "Number of Drivers Based on Vehicle Licenses Type, 2015-2021")

fig <- fig %>% config(displayModebar = F)

fig <- fig %>% layout(margin = list(b=160),
                      annotations=list(text='Data Source: <a href="https://www1.nyc.gov/site/tlc/about/aggregated-reports.page", target="blank">NYCTLC</a>', 
                                       font=list(size=11),
                                       showarrow=F,
                                       x=1,
                                       xanchor='right',
                                       xref='paper',
                                       y=-0.3,
                                       yanchor='top',
                                       yref='paper'))

fig <- fig %>% layout(yaxis=list(ticklen = 10, tickcolor = "transparent"))

fig

path = "C:/Users/S_Sanich/Desktop/td-trends/fhv"

htmlwidgets::saveWidget(fig,paste0(path,"license_types.html"))
