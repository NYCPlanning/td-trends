library(tidyverse)
library(ggplot2)
library(plotly)

url = "https://new.mta.info/document/20441"

df2 = df=read.csv(url,colClasses='character',stringsAsFactors=F)

ggplot(data=df2) + geom_point(mapping=aes(x = Date, y = Subways..Total.Estimated.Ridership))

df2=df2 %>%
  +     mutate(Date=as.Date(Date,'%m/%d/%Y')) %>%
  +     mutate(Subway=as.integer(Subways..Total.Estimated.Ridership)) %>%
  +     arrange(Date) %>%
  +     select(Date,Subway) %>%
  +     gather(key=Type,value=Ridership,c('Subway')) %>%
  +     mutate(Type2=factor(Type,levels=c('Subway')))   

p2=ggplot(data=df2, aes(x=Date, y=Ridership, group=1))+
  + geom_line()+
  + geom_point()

p2

library(scales)

ggp+
  + scale_y_continuous(labels = comma) +
  + ggtitle ("Daily Subway Ridership During COVID-19")

               