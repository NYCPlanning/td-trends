library("tidyverse")
library("ggplot2")
library("plotly")
library("scales")
install.packages("tibble")
library("tibble")

install.packages("reshape")
library("reshape")

df = AnnualBusRidership

head(df)


ggp <- df %>%
  gather(key="group", value="values", -Year) %>%
  ggplot(aes(x=Year, y=values, color=group)) +
  geom_point()+
  geom_line()+
  scale_y_continuous(labels = comma)+
  ggtitle("Annual Bus Ridership")+
  theme(panel.background = element_blank())+
  labs(x= "Year", y="Ridership", title = "Annual Bus Ridership", caption = "Source: MTA")+
  scale_fill_discrete(name="Borough", labels = c("Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island"))

ggp





  
