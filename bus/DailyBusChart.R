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
         Bus=as.numeric(df[['Buses: Total Estimated Ridership']]),
         BusPrior=Bus/as.numeric(str_replace(df[['Buses: % of Comparable Pre-Pandemic Day']],'%',''))*100,
         BusPctPrior=Bus/BusPrior) %>%
  select(Date,Bus,BusPrior,BusPctPrior) %>%
  arrange(Date)

df=df %>%
  mutate(Bus1=c(NA,df[1:nrow(df)-1,'Bus']),
         Bus2=c(NA,NA,df[2:nrow(df)-2,'Bus']),
         Bus3=c(NA,NA,NA,df[3:nrow(df)-3,'Bus']),
         Bus4=c(NA,NA,NA,NA,df[4:nrow(df)-4,'Bus']),
         Bus5=c(NA,NA,NA,NA,NA,df[5:nrow(df)-5,'Bus']),
         Bus6=c(NA,NA,NA,NA,NA,NA,df[6:nrow(df)-6,'Bus']),
         Bus7DayAvg=rowMeans(cbind(Bus,Bus1,Bus2,Bus3,Bus4,Bus5,Bus6)),
         BusPrior1=c(NA,df[1:nrow(df)-1,'BusPrior']),
         BusPrior2=c(NA,NA,df[2:nrow(df)-2,'BusPrior']),
         BusPrior3=c(NA,NA,NA,df[3:nrow(df)-3,'BusPrior']),
         BusPrior4=c(NA,NA,NA,NA,df[4:nrow(df)-4,'BusPrior']),
         BusPrior5=c(NA,NA,NA,NA,NA,df[5:nrow(df)-5,'BusPrior']),
         BusPrior6=c(NA,NA,NA,NA,NA,NA,df[6:nrow(df)-6,'BusPrior']),
         Bus7DayAvgPrior=rowMeans(cbind(BusPrior,BusPrior1,BusPrior2,BusPrior3,BusPrior4,BusPrior5,BusPrior6)),
         Bus7DayAvgPctPrior=Bus7DayAvg/Bus7DayAvgPrior) %>%
  select(Date,Bus,BusPrior,BusPctPrior,Bus7DayAvg,Bus7DayAvgPrior,Bus7DayAvgPctPrior)
write.csv(df,paste0(path,'bus/Bus7DayAverage.csv'),na='NA',row.names=F)


df=read.csv(paste0(path,'bus/Bus7DayAverage.csv'),stringsAsFactors=F,colClasses=c('Date','numeric','numeric','numeric','numeric','numeric','numeric'))
p=plot_ly()
p=p %>%
  add_trace(type='bar',
            x=df[['Date']],
            y=df[['Bus']],
            opacity=0,
            showlegend=F,
            hovertext=paste0('<b>Date: </b>',format(df[['Date']],'%m/%d/%Y',trim=T)),
            hoverinfo='text')
p=p %>%
  add_trace(name='Daily Ridership',
            type='bar',
            x=df[['Date']],
            y=df[['Bus']],
            marker=list(color='rgba(103,191,92,0.6)'),
            showlegend=T,
            hovertext=paste0('<b>Daily Ridership: </b>',format(df[['Bus']],trim=T,big.mark=','),' (',format(round(df[['BusPctPrior']]*100,1),trim=T,nsmall=1),'%)'),
            hoverinfo='text')
p=p %>%
  add_trace(name='7-Day Moving Average',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Bus7DayAvg']],
            line=list(color='rgba(237,102,93,0.8)',
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>7-Day Moving Average: </b>',format(df[['Bus7DayAvg']],trim=T,big.mark=','),' (',format(round(df[['Bus7DayAvgPctPrior']]*100,1),trim=T,nsmall=1),'%)'),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Daily Bus Ridership</b>'),
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
                    range=c(min(df[['Date']])-15,max(df[['Date']])+15),
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
         hoverlabel=list(bgcolor='rgba(255,255,255,0.95)',
                         bordercolor='rgba(0,0,0,0.1)',
                         font=list(size=14)),
         font=list(family='Arial',
                   color='black'),
         dragmode=F,
         hovermode='x unified')
p=p %>% 
  add_annotations(text='Data Source: <a href="https://new.mta.info/coronavirus/ridership" target="blank">MTA</a> | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/bus/Bus7DayAverage.csv" target="blank">Download Chart Data</a>',
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
  config(displayModeBar=T,
         displaylogo=F,
         modeBarButtonsToRemove=c('select','lasso2d'))
p
htmlwidgets::saveWidget(p,paste0(path,'bus/DailyBusChart.html'))


