library(tidyverse)
library(plotly)
library(tibble)


Year <- c(2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)
Domestic_Freight <- c(1082384, 962975, 799745, 843903, 811377, 774842, 700393, 679116, 707657, 753926, 800548, 838227, 851209, 889740)
International_Freight <- c(1554326, 1406782, 1141324, 1431313, 1407661, 1313381, 1308008, 1353169, 1352483, 1334961, 1444261, 1460898, 1342454, 988177)
Total_Freight <- c(2636710, 2369756, 1941069, 2275216, 2219038, 2088223, 2008401, 2032285, 2060140, 2088887, 2244809, 2299125, 2193664, 1877917)

df <- data.frame(Year, Domestic_Freight, International_Freight)

p=plot_ly()

p=p %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["Domestic_Freight"]], name = "Domestic Freight", hovertemplate="%{y:,.0f}") %>%
  add_trace(type="scatter", mode="lines", x=df[["Year"]], y=df[["International_Freight"]], name = "International Freight", hovertemplate="%[y:,.0f") %>%
  layout(title = "Annual Revenue Freight", xaxis=list(title="Date"), yaxis=list(title="Freight (in short tons)")) %>%
  layout(margin = list(b=160), annotations=list(x=1, y=-0.2, text= "Data Source: Port Authority of NY & NJ", showarrow=F, xref="paper", yref="paper",
                                                xanchor="right", yanchor="top", xshift=0, yshift=0, font=list(size=12, color="grey"))) %>%
  config(displayModeBar = F)

p


