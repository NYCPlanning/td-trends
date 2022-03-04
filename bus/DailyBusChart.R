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
         Bus=as.numeric(df[['Buses: Total Estimated Ridership']])) %>%
  select(Date,Bus) %>%
  arrange(Date)

df=df %>%
  mutate(Bus1=c(NA,df[1:nrow(df)-1,'Bus']),
         Bus2=c(NA,NA,df[2:nrow(df)-2,'Bus']),
         Bus3=c(NA,NA,NA,df[3:nrow(df)-3,'Bus']),
         Bus4=c(NA,NA,NA,NA,df[4:nrow(df)-4,'Bus']),
         Bus5=c(NA,NA,NA,NA,NA,df[5:nrow(df)-5,'Bus']),
         Bus6=c(NA,NA,NA,NA,NA,NA,df[6:nrow(df)-6,'Bus']),
         Bus7DayAverage=rowMeans(cbind(Bus,Bus1,Bus2,Bus3,Bus4,Bus5,Bus6))) %>%
  select(Date,Bus,Bus7DayAverage)
write.csv(df,paste0(path,'bus/Bus7DayAverage.csv'),na='NA',row.names=F)


df=read.csv(paste0(path,'bus/Bus7DayAverage.csv'),stringsAsFactors = F,colClasses = c('Date','numeric','numeric'))
p=plot_ly()
p=p %>%
  add_trace(name='Daily Ridership',
            type='bar',
            x=df[['Date']],
            y=df[['Bus']],
            marker=list(color='rgba(114,158,206,0.5)'),
            showlegend=T,
            hovertemplate='%{y:,.0f}',
            xhoverformat='<b>%m/%d/%Y</b>')
p=p %>%
  add_trace(name='7-Day Moving Average',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Bus7DayAverage']],
            line=list(color='rgba(237,102,93,0.8)',
                      width=3),
            showlegend=T,
            hovertemplate='%{y:,.0f}',
            xhoverformat='<b>%m/%d/%Y</b>')
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
  config(displayModeBar=F)
p
htmlwidgets::saveWidget(p,paste0(path,'bus/DailyBusChart.html'))


