from dash import Dash, html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import json

df = pd.read_csv("F:\study\projects\COVID-19 Dashboard - Power BI\COVID-19_Dashboard\data\local_situation.csv")
df2 = pd.read_csv("F:\study\projects\COVID-19 Dashboard - Power BI\COVID-19_Dashboard\data\District and MOH cases.csv",
                  dtype={"State": int})
with open('F:\study\projects\COVID-19 Dashboard - Power BI\COVID-19_Dashboard\data\geo_data.json') as response:
    states = json.load(response)

# Create a Dash app & Linking bootstrap stylesheet
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], title="Covid-19 Dashboard")

# Convert Date column to datetime format
#df['Date'] = pd.to_datetime(df['Date'])

lineChart = px.line(
        df,
        x="Date",
        y=["Total Number of Deaths", "Total Number Confirmed", "Total Number Recovered", "Number inward as at today-10 am"],
        title="Breakdown of Total Cases in Sri Lanka",
)

lineChart.update_layout(
    font_family="DIN",  
    font_color="black",  
    plot_bgcolor="#f6f6f6",  
    paper_bgcolor="#fff",  
    margin=dict(l=40, r=40, t=40, b=20),
    xaxis_nticks=10,
    yaxis_title="Cases" 
)

variable_names = {'Total Number of Deaths':'Total Deaths', 
                  'Total Number Confirmed':'Total Confirmed Cases', 
                  'Total Number Recovered':'Total Recoveries',
                  'Number inward as at today-10 am':'Active Cases'}
lineChart.for_each_trace(lambda t: t.update(name = variable_names[t.name],
                                      legendgroup = variable_names[t.name],
                                      hovertemplate = t.hovertemplate.replace(t.name, variable_names[t.name])))
fig = px.choropleth_mapbox(
    df2,
    geojson=states,
    locations='State',  
    color="cases",
    color_continuous_scale="viridis_r",
    range_color=(0, 50000),  
    mapbox_style="carto-positron",  
    title="COVID-19 Cases in Sri Lanka",
    zoom=8,
    center = {"lat": 7.637034, "lon": 80.023362},  
    hover_name="MOH/QC/Camp",  
    hover_data=["MOH/QC/Camp", "cases"],
    opacity=0.5,
    labels={'MOH/QC/Camp':'cases'}  
)

fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})  

# Optional: Add a colorbar
fig.update_layout(coloraxis_colorbar=dict(title="Number of Cases"))

# Define the layout of the app
app.layout = html.Div([ 
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.Img(src='assets\logo.jpg', width=100, height=100, style={"float":"right"}),
                width="auto",
                style={"border":"1px solid black"} ,
                #class_name="mx-auto"                         
            ),
            dbc.Col(
                html.H1(
            "COVID-19: Situational Analysis",            
            style={"font-family":"Lucida Sans Unicode", "text-align":"center"}),
            width="auto",
            style={"border":"1px solid black"},
            #class_name="mx-auto"  
            )       
        ], style={"border":"1px solid black", "float":"center"}, class_name="mx-auto" ), #style={"text-align":"center"}    
        dbc.Card([
            dcc.Graph(id="line-chart", figure=lineChart),
            dcc.Graph(id="map-lanka",figure=fig)
        ]),
        dcc.Markdown("Above data is only up to 2021-May-18")
    ], style={"padding-top":"15px"})   
], style={"background-color":"#f6f6f6"})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)