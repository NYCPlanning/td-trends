p=plot_ly()

p=p %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Year"]], 
            y=df[["Domestic_Freight"]], 
            name = "<b>Domestic Freight</b>",
            hovertemplate="%{y:,.0f}",
            color = "#729ece") %>%
  add_trace(type="scatter", 
            mode="lines", 
            x=df[["Year"]], 
            y=df[["International_Freight"]], 
            name = "<b>International Freight</b>", 
            hovertemplate="%{y:,.0f}",
            color = "#ff9e4a") %>%
  layout(title = "<b>Annual Revenue Freight</b>", 
         xaxis=list(title="<b>Date</b>"), 
         yaxis=list(title="<b>Freight (in short tons)</b>")) %>%
  layout(margin = list(b=160), 
         annotations=list(x=1, y=-0.2, 
                          text= "Data Source: <a href='https://www.panynj.gov/airports/en/statistics-general-info.html' target='blank'>Port Authority of NY & NJ</a>", 
                          showarrow=F, 
                          xref="paper", yref="paper",
                          xanchor="right", yanchor="top", 
                          xshift=0, yshift=0, 
                          font=list(size=12, color="grey"))) %>%
  layout(xaxis=list(showgrid=FALSE)) %>%
  config(displayModeBar = F)

p


path = "C:/Users/S_Sanich/Desktop/td-trends/air"

htmlwidgets::saveWidget(p,paste0(path,"air_freight.html"))

