library(tidyverse)
library(plotly)
library(tibble)


Year <- c(1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 
          2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020)
Domestic <- c(54546489, 54131912, 49657706, 52181778, 52765365, 56810244, 56113208, 58298553, 60263053, 61160266, 62370619, 64364631, 58503949, 57548096, 60054449, 66825850, 70621497, 
              73415495, 76501093, 72147681, 68096986, 68458586, 69446991, 71691699, 72889743, 74250618, 79464738, 83814838, 85073562, 88071899, 89479096, 28339519)
International <- c(19862851, 20682044, 18533027, 19609229, 19645463, 20759576, 22203938, 23403575, 24366877, 25805085, 27249900, 28414615, 24750553, 23826404, 24016163, 27606745, 
                   29636571, 30968851, 33524127, 34869256, 33684380, 35626880, 36430110, 37638192, 39569574, 41795017, 43635938, 45914209, 47645467, 50196394, 51019037, 12526599)
Total <- c(74409340, 74813956, 68190733, 71791007, 72410828, 77569820, 78317146,  81702128, 84629930, 86965351, 89620519, 92779246, 83254502, 81374500, 84070612, 94432595, 100258068,
           104384346, 110025220, 107016937, 101781366, 104085466, 105877101, 109329891, 112459317, 116045635, 123100676, 129729047, 132719029, 138268293, 140498133, 40866118)

df <- data.frame(Year, Domestic, International, Total)

fig <- plot_ly(df,
               x= ~Year, y= ~International, 
               type = "bar", 
               name = "<b>International Flights", 
               marker = list(color = "#6dccda", 
                             showticklabels=TRUE))
fig <- fig %>% add_trace(y = ~Domestic, 
                         name = "<b>Domestic Flights", 
                         marker = list(color="#cdcc5d"))
fig <- fig %>% layout(yaxis = list(title = "<b>Number of Passengers"), barmode = "stack")
fig <- fig %>% layout(title = "<b>Annual Air Passenger Traffic")
fig <- fig %>% config(displayModeBar = F)
fig <- fig %>% layout(margin = list(b=160), 
                      annotations=list(x=1, y=-0.2, 
                                       text= "Data Source: <a href='https://www.panynj.gov/airports/en/statistics-general-info.html' target='blank'>Port Authority of NY and NJ</a>", 
                                       showarrow=F, 
                                       xref="paper", yref="paper",
                                       xanchor="right", yanchor="top", 
                                       xshift=0, yshift=0, 
                                       font=list(size=12, 
                                                 color="grey")))

fig

path = "C:/Users/S_Sanich/Desktop/td-trends/air"

htmlwidgets::saveWidget(p,paste0(path,"annual_air_domesticvinternational.html"))
