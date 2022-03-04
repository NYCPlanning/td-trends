library(tidyverse)
library(plotly)


# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'


url='https://new.mta.info/document/20441'
download.file(url,destfile='temp.csv')
df=read.csv('temp.csv',stringsAsFactors=F,check.names=F)
file.remove('temp.csv')

df=df %>%
  mutate(Date=as.Date(df[['Date']], "%m/%d/%Y"),
         Subway=as.numeric(df[['Subways: Total Estimated Ridership']]),
         SubwayPrior=Subway/as.numeric(str_replace(df[['Subways: % of Comparable Pre-Pandemic Day']],'%',''))*100,
         SubwayPctPrior=Subway/SubwayPrior) %>%
  select(Date,Subway,SubwayPrior,SubwayPctPrior) %>%
  arrange(Date)

df=df %>%
  mutate(Subway1=c(NA,df[1:nrow(df)-1,'Subway']),
         Subway2=c(NA,NA,df[2:nrow(df)-2,'Subway']),
         Subway3=c(NA,NA,NA,df[3:nrow(df)-3,'Subway']),
         Subway4=c(NA,NA,NA,NA,df[4:nrow(df)-4,'Subway']),
         Subway5=c(NA,NA,NA,NA,NA,df[5:nrow(df)-5,'Subway']),
         Subway6=c(NA,NA,NA,NA,NA,NA,df[6:nrow(df)-6,'Subway']),
         Subway7DayAvg=rowMeans(cbind(Subway,Subway1,Subway2,Subway3,Subway4,Subway5,Subway6)),
         SubwayPrior1=c(NA,df[1:nrow(df)-1,'SubwayPrior']),
         SubwayPrior2=c(NA,NA,df[2:nrow(df)-2,'SubwayPrior']),
         SubwayPrior3=c(NA,NA,NA,df[3:nrow(df)-3,'SubwayPrior']),
         SubwayPrior4=c(NA,NA,NA,NA,df[4:nrow(df)-4,'SubwayPrior']),
         SubwayPrior5=c(NA,NA,NA,NA,NA,df[5:nrow(df)-5,'SubwayPrior']),
         SubwayPrior6=c(NA,NA,NA,NA,NA,NA,df[6:nrow(df)-6,'SubwayPrior']),
         Subway7DayAvgPrior=rowMeans(cbind(SubwayPrior,SubwayPrior1,SubwayPrior2,SubwayPrior3,SubwayPrior4,SubwayPrior5,SubwayPrior6)),
         Subway7DayAvgPctPrior=Subway7DayAvg/Subway7DayAvgPrior) %>%
  select(Date,Subway,SubwayPrior,SubwayPctPrior,Subway7DayAvg,Subway7DayAvgPrior,Subway7DayAvgPctPrior)
write.csv(df,paste0(path,'subway/Subway7DayAverage.csv'),na='NA',row.names=F)


df=read.csv(paste0(path,'subway/Subway7DayAverage.csv'),stringsAsFactors=F,colClasses=c('Date','numeric','numeric','numeric','numeric','numeric','numeric'))
p=plot_ly()
p=p %>%
  add_trace(type='bar',
            x=df[['Date']],
            y=df[['Subway']],
            opacity=0,
            showlegend=F,
            hovertext=paste0('<b>Date: </b>',format(df[['Date']],'%m/%d/%Y',trim=T)),
            hoverinfo='text')
p=p %>%
  add_trace(name='Daily Ridership',
            type='bar',
            x=df[['Date']],
            y=df[['Subway']],
            marker=list(color='rgba(114,158,206,0.5)'),
            showlegend=T,
            hovertext=paste0('<b>Daily Ridership: </b>',format(df[['Subway']],trim=T,big.mark=','),' (',round(df[['SubwayPctPrior']]*100,1),'%)'),
            hoverinfo='text')
p=p %>%
  add_trace(name='7-Day Moving Average',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Subway7DayAvg']],
            line=list(color='rgba(237,102,93,0.8)',
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>7-Day Moving Average: </b>',format(df[['Subway7DayAvg']],trim=T,big.mark=','),' (',round(df[['Subway7DayAvgPctPrior']]*100,1),'%)'),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Daily Subway Ridership</b>'),
                    font=list(size=20),
                    x=0.5,
                    xanchor='center',
                    y=0.95,
                    yanchor='top'),
         legend=list(orientation='h',
                     title=list(text=''),
                     font=list(size=16),
                     x=0.5,
                     xanchor='center',
                     y=1,
                     yanchor='bottom'),
         margin=list(b=120,
                     l=80,
                     r=40,
                     t=120),
         xaxis=list(title=list(text='<b>Date</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    tickformat='%b %Y',
                    dtick='M2',
                    range=c(min(df[['Date']])-10,max(df[['Date']])+10),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Ridership</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         hoverlabel=list(font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://new.mta.info/coronavirus/ridership" target="blank">MTA</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/subway/Subway7DayAverage.csv" target="blank">Download Chart Data</a>',
                  font=list(size=14),
                  showarrow=F,
                  x=1,
                  xanchor='right',
                  xref='paper',
                  y=0,
                  yanchor='top',
                  yref='paper',
                  yshift=-80)
p=p %>%
  config(displayModeBar=F)
p
htmlwidgets::saveWidget(p,paste0(path,'subway/DailySubwayChart.html'))


