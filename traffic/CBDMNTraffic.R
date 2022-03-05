library(tidyverse)
library(plotly)

# path='C:/Users/Y_Ma2/Desktop/GITHUB/td-trends/'
path='C:/Users/mayij/Desktop/DOC/GITHUB/td-trends/'

df=read.csv(paste0(path,'traffic/CBDMN2019_2021.csv'),stringsAsFactors=F,check.names=F)
df=df %>%
  mutate(Date=as.Date(Date,'%m/%d/%Y')) %>%
  select(Date,TBTA_CBDInbound_Avg,PANYNJ_CBDInbound_Avg,ERB_Inbound_Avg,TPEP_CBD_Speed_Avg)
colnames(df)=c('Date','MTA Bridges & Tunnels','PANYNJ Bridges & Tunnels','East River Bridges','Taxi Speed')

dfcolors=c('MTA Bridges & Tunnels'='rgba(114,158,206,0.8)',
           'PANYNJ Bridges & Tunnels'='rgba(255,158,74,0.8)',
           'East River Bridges'='rgba(103,191,92,0.8)')

p=plot_ly()
p=p %>%
  add_trace(name='Taxi Speed',
            type='scatter',
            mode='lines',
            x=df[['Date']],
            y=df[['Taxi Speed']],
            yaxis='y2',
            line=list(color='rgba(237,102,93,0.8)',
                      width=3),
            showlegend=T,
            hovertext=paste0('<b>Taxi Speed: </b>',format(round(df[['Taxi Speed']],2),trim=T,nsmall=2)),
            hoverinfo='text')
for (i in c('MTA Bridges & Tunnels','PANYNJ Bridges & Tunnels','East River Bridges')){
  p=p %>%
    add_trace(name=i,
              type='scatter',
              mode='none',
              x=df[['Date']],
              y=df[[i]],
              showlegend=T,
              stackgroup='one',
              groupnorm='',
              orientation='v',
              fill='tonexty',
              fillcolor=dfcolors[i],
              hovertext=paste0('<b>',i,': </b>',format(df[[i]],trim=T,big.mark=',')),
              hoverinfo='text')
}
p=p %>%
  add_trace(type='scatter',
            mode='none',
            x=df[['Date']],
            y=df[['MTA Bridges & Tunnels']],
            showlegend=F,
            hovertext=paste0('<b>Date: </b>',format(df[['Date']],'%m/%d/%Y')),
            hoverinfo='text')
p=p %>%
  layout(template='plotly_white',
         title=list(text=paste0('<b>Manhattan CBD Traffic Volumn and Speed <br>(7-Day Moving Average)</b>'),
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
                     y=0.95,
                     yanchor='bottom'),
         margin=list(b=120,
                     l=80,
                     r=80,
                     t=120),
         xaxis=list(title=list(text='<b>Date</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    tickformat='%b %Y',
                    dtick='M1',
                    range=c(min(df[['Date']])-15,max(df[['Date']])+15),
                    fixedrange=T,
                    showgrid=F),
         yaxis=list(title=list(text='<b>Daily Inbound Volume</b>',
                               font=list(size=14)),
                    tickfont=list(size=12),
                    rangemode='tozero',
                    fixedrange=T,
                    showgrid=T,
                    zeroline=T,
                    zerolinecolor='rgba(0,0,0,0.2)',
                    zerolinewidth=2),
         yaxis2=list(title=list(text='<b>Speed (mph)</b>',
                                font=list(size=14)),
                     tickfont=list(size=12),
                     rangemode='tozero',
                     side='right',
                     overlaying='y',
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
  add_annotations(text='Data Source: NYC DOT | <a href="https://raw.githubusercontent.com/NYCPlanning/td-trends/main/traffic/CBDMN2019_2021.csv" target="blank">Download Chart Data</a>',
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
htmlwidgets::saveWidget(p,paste0(path,'traffic/CBDMNTraffic.html'))




