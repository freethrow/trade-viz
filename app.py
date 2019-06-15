# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask import Flask



import plotly.plotly as py
import pandas as pd

import plotly.graph_objs as go

from dash.dependencies import Input, Output

from utilities import *

(dr, legend)=series_countries_per_category(['Germany','Italy','China'],'export_value', 'All')

topN = top_N_countries(5)

topNcats = top_N_sectors(N=5, year=2018, flux='exchange', country='All')




all_countries = commerce.country.unique()
country_opts = []
for cnt in all_countries:
    country_opts.append({'label':cnt, 'value':cnt})

country_opts.insert(0, {'label':'World', 'value':'All'})

from textwrap import dedent

all_categories = commerce.category.unique()
category_opts = []
for cnt in all_categories:
    category_opts.append({'label':cnt, 'value':cnt})


all_years = range(2004,2019)
years_opts = []
for cnt in all_years:
    years_opts.append({'label':cnt, 'value':cnt})


category_opts.insert(0, {'label':'All categories', 'value':'All'})




m=data_mapper(flux = 'export_value')



map_data = [go.Choropleth(
    locations = m['ccode'],
    z = m['export_value'],
    text = m['country'],
    colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'],
        [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
        [0.6666666666666666, 'rgb(171,217,233)'],[0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'],
        [1.0, 'rgb(49,54,149)']],
    #colorscale = 'YlGnBu',
    autocolorscale = False,
    reversescale = False,
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(180,180,180)',
            width = 0.5
        )),
    colorbar = go.choropleth.ColorBar(
        tickprefix = '$',
        title = 'Trade<br>Thousands US$'),
)]

map_layout = go.Layout(
    title = go.layout.Title(
        text = 'Serbian Foreign Trade'
    ),
    width=900,
    height=600,
    geo = go.layout.Geo(
        showframe = False,
        showcoastlines = False,
        projection = go.layout.geo.Projection(
            type = 'equirectangular'
        )
    ),
    annotations = [go.layout.Annotation(
        x = 0.55,
        y = 0.1,
        xref = 'paper',
        yref = 'paper',
        text = 'Source: <a href="http://www.stat.gov.rs/">\
            Statistical Office of The Republic Of Serbia</a>',
        showarrow = False
    )]
)




navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Contact", href="mailto:aleksendric@gmail.com")),
        
        
    ],
    brand="Interactive Data Visualization - Serbian Foreign Trade",
    brand_href="https://serbian-trade.herokuapp.com/",
    sticky="top"
)

body = dbc.Container(
    [
        dbc.Row(
            [

      
                dbc.Col(
                    [
                        html.H2("Foreign Trade Serbia", className='text-center'),
                        dcc.Markdown(dedent('''

                            #### Select the countries by typing them and hitting TAB, the category (or "All"), the flow type.

                            This chart enables you to visually compare the trade with Serbia between different countries (or "All") for
                            the selected category (or "All").
                            '''), className="alert alert-dark m-5"),
                        html.P("Select the country or countries"),
                        dcc.Dropdown(
                            id='country-selector',
                            options=country_opts,
                            value=['All'],
                            multi=True
                                        ),
                        html.P("Select the category or all categories"),
                        dcc.Dropdown(
                            id='category-selector',
                            options=category_opts,
                            value='All',
                            multi=False
                                        ),
                         html.P("Select the flow (export/import/exchange"),
                        dcc.Dropdown(
                            id='drop-down',
                            options=[
                                {'label': 'Serbian Exports', 'value': 'exp'},
                                {'label': 'Serbian Imports', 'value': 'imp'},
                                {'label': 'Serbian Exchange', 'value': 'exc'},
                                {'label': 'Serbian Trade Balance', 'value': 'bal'}
                                    ],
                            value='exp'
                                        ),
                        dcc.RadioItems(
                                id='chart-type',
                                options=[
                                    {'label': 'Bar Chart', 'value': 'bar'},
                                    {'label': 'Line Chart', 'value': 'line'}
                                ],
                                value='bar',
                                className='m-2'
                            ),
                        dcc.RadioItems(
                                id='chart-stacked',
                                options=[
                                    {'label': 'Side by side', 'value': 'side'},
                                    {'label': 'Stacked', 'value': 'stacked'}
                                ],
                                value='side',
                                className='m-2'
                            ),
                        dcc.Graph(
                            id='example-graph',
                            className='fig',
                            figure={
                                'data': dr,
                                'layout': {
                                    'title': legend
                                }
                            }
                        )
                    ]
                ),
            

           
            ]
        ),

               dbc.Row(
            [

            

            dbc.Col(
                    [
                        html.H2("Category drilldown", className='text-center'),
                        dcc.Markdown(dedent('''

                            #### Select the category, the top N number, the flow type and the year

                            This chart enables you to visualize the top N countries in the selected type of trade. Move the slider to choose
                            the top N number of countries. The barchart adds up to 100%, so the rest is calculated by subtracting the sum 
                            of the top N countries values from the total trade.
                            '''), className="alert alert-dark m-5"),
                        html.P("Select the trade category"),
                        dcc.Dropdown(
                            id='category-drilldown-selector',
                            options=category_opts,
                            value='All',
                            multi=False
                                        ),
                        html.P("Select the flow type", className='mt-2'),
                        dcc.Dropdown(
                            id='flow-drilldown-selector',
                            options=[
                                {'label': 'Serbian Exports', 'value': 'export_value'},
                                {'label': 'Serbian Imports', 'value': 'import_value'},
                                {'label': 'Serbian Exchange', 'value': 'exchange'},
                                {'label': 'Serbian Trade Balance', 'value': 'balance'}
                                    ],
                            value='exchange'),
                        html.P("Select the top N number"),
                        dcc.Slider(
                            id="drilldown-slider",
                            min=3,
                            max=10,
                            marks={i: '{}'.format(i) for i in range(3,11)},
                            value=5,
                            className='m-3'
                        ),
                        html.P("Select the year",className='mt-2'),
                        dcc.Dropdown(
                            id='drilldown-year-slider',
                            options=years_opts,
                            multi=False,
                            value=2018,
                            className='mt-2'
                        ),

                        dcc.Graph(
                            id='drilldown-graph',
                            className='fig',
                            figure={
                                'data': 
                                [
                                {
                                "values": topN.values,
                                "labels": topN.index,
                                "domain": {"column": 0},
                                "name": "Top N",
                                "hoverinfo":"label+value+name",
                                "hole": .4,
                                "type": "pie"
                                }],
                                'layout': {
                                    'title': 'Mus'
                                }
                            }
                        ),

                        html.H2("World Map ", className='text-center'),
                        dcc.Markdown(dedent('''

                            #### Select the category, the flow type and the year

                            A visual exploration of the Serbian foreign trade. The red colors indicate a **lower** value, while
                            the blues mark the countries with a **higher** value in the selected type of trade.
                            '''), className="alert alert-dark m-5"),
                        html.P("Select the trade category"),
                        dcc.Dropdown(
                            id='category-map',
                            options=category_opts,
                            value='All',
                            multi=False
                                        ),
                        html.P("Select the flow type", className='mt-2'),
                        dcc.Dropdown(
                            id='flow-map',
                            options=[
                                {'label': 'Serbian Exports', 'value': 'export_value'},
                                {'label': 'Serbian Imports', 'value': 'import_value'},
                                {'label': 'Serbian Exchange', 'value': 'exchange'},
                                {'label': 'Serbian Trade Balance', 'value': 'balance'}
                                    ],
                            value='exchange'),
                       
                        html.P("Select the year",className='mt-2'),
                        dcc.Dropdown(
                            id='year-map',
                            options=years_opts,
                            multi=False,
                            value=2018,
                            className='mt-2'
                        ),
                        
                     

                         dcc.Graph(
                            id='map-graph',
                            className='fig',
                            figure={
                                'data': map_data,
                                'layout': map_layout
                            }
                        ),

                       
                    ]
                ),
            ]
        ),

               dbc.Row(
            [

            

            dbc.Col(
                    [
                        html.H2("Country drilldown", className='text-center'),
                        dcc.Markdown(dedent('''

                            #### Select the country, the top N number, the flow type and the year

                            This chart enables you to visualize the main categories (top N) that compose the selected type of trade.
                            Move the slider to choose the top N number of categories. The barchart adds up to 100%, so the rest is calculated by subtracting the sum 
                            of the top N categories values from the total trade.
                            '''), className="alert alert-dark m-5"),
                        html.P("Select the country"),
                        dcc.Dropdown(
                            id='country-drilldown-selector',
                            options=country_opts,
                            value='All',
                            multi=False
                                        ),
                        html.P("Select the flow type", className='mt-2'),
                        dcc.Dropdown(
                            id='flow-drilldown-selector-2',
                            options=[
                                {'label': 'Serbian Exports', 'value': 'export_value'},
                                {'label': 'Serbian Imports', 'value': 'import_value'},
                                {'label': 'Serbian Exchange', 'value': 'exchange'},
                                {'label': 'Serbian Trade Balance', 'value': 'balance'}
                                    ],
                            value='exchange'),
                        html.P("Select the top N number"),
                        dcc.Slider(
                            id="drilldown-slider-2",
                            min=3,
                            max=10,
                            marks={i: '{}'.format(i) for i in range(3,11)},
                            value=5,
                            className='m-3'
                        ),
                        html.P("Select the year",className='mt-2'),
                        dcc.Dropdown(
                            id='drilldown-year-slider-2',
                            options=years_opts,
                            multi=False,
                            value=2018,
                            className='mt-2'
                        ),
                        
                        dcc.Graph(
                            id='drilldown-graph-2',
                            className='fig',
                            figure={
                                'data': 
                                [
                                {
                                "values": topNcats.values,
                                "labels": topNcats.index,
                                "domain": {"column": 0},
                                "name": "Top N",
                                "hoverinfo":"label+value+name",
                                "hole": .4,
                                "type": "pie"
                                }],
                                'layout': {
                                    'title': 'Mus'
                                }
                            }
                        ),

                        dcc.Markdown(dedent('''

                            ### Interactive Serbian Trade Data

                            This is a project by Marko Aleksendrić, PhD, based on the [Statistical Office of the Republic of Serbia](http://www.stat.gov.rs/en-US/) open
                            trade statistics dataset. It aims to provide an intuitive and direct way of interacting with the underlying data, enabling the user to ask questions and 
                            get a **quick, intuitive and visual response**. Playing with the data is probably the best way to understand it.
                            ***
                            The application is based on [Dash](https://dash.plot.ly), which on the other hand, relies on Plotly, React and Flask.
                            The making of this app is documented in the Jupyter Notebook with the data wrangling [here](http://github.com/freethrow).
                            The Statistical Office of the Republic of Serbia provides a dataset that spans from 2004 through 2018 and it is accessible and
                            downloadable in a csv or json format.
                            ***
                            **The data is provided by the [Statistical Office of the Republic of Serbia](http://opendata.stat.gov.rs/odata/)**.
                            ***
                            Coded by [freethrow.rs](http://www.freethrow.rs) in 2019.
                  
                            '''), className="alert alert-dark footer")
                    ]
                ),
            ]
        ),


    ],
    className="mt-4",
)


server = Flask(__name__)
server.secret_key = 'somevelvetmorning'

app = dash.Dash(__name__, server = server, external_stylesheets=[dbc.themes.JOURNAL])

app.layout = html.Div([navbar, body])

app.title = "Data Visualization - Serbian Foreign Trade 2004 - 2018"


@app.callback(
    Output(component_id='example-graph', component_property='figure'),
    [Input(component_id='drop-down', component_property='value'),
    Input(component_id='chart-type', component_property='value'),
    Input(component_id='chart-stacked', component_property='value'),
    Input(component_id='country-selector', component_property = 'value'),
    Input(component_id='category-selector', component_property = 'value')]
)
def update_bar_chart(select_flow, chart_type, chart_stacked, countries, category):

    if countries ==[]:
        countries = ['All']

    if (select_flow == 'imp'):

        (dr, legend)=series_countries_per_category(countries,'import_value', category, chart_type)
              
    elif (select_flow == 'exp'):
        
        (dr, legend)=series_countries_per_category(countries,'export_value', category, chart_type)

    elif (select_flow == 'bal'):
        
        (dr, legend)=series_countries_per_category(countries,'balance', category, chart_type)

    else:
        (dr, legend)=series_countries_per_category(countries,'exchange', category,chart_type)

    if chart_stacked == 'stacked':
        barmode = 'stack'
    else:
        barmode = 'group'

    return {"data": dr,
            'layout': {
                'title': legend,
                'barmode': barmode,
                 'colorway':["#4f9da6", "#facf5a","#ff5959","#930077","#233142"],
            }
            }


@app.callback(
    Output(component_id='drilldown-graph', component_property='figure'),
    [Input(component_id='category-drilldown-selector', component_property='value'),
    Input(component_id='drilldown-slider', component_property='value'),
    Input(component_id='flow-drilldown-selector', component_property = 'value'),
    Input(component_id='drilldown-year-slider', component_property='value'),]
)
def update_drilldown(category, num ,flow, year):


    if category ==None:
        category ='All'


    topN = top_N_countries(N=num, category = category, year = year, flux = flow)


    data=[
               {
                "values": topN.values,
                "labels": topN.index,
                "domain": {"column": 0},
                "name": "Top "+str(num),
                "hoverinfo":"label+value+name",
                "hole": .5,
                "type": "pie"
                }]
    
    if flow == 'exchange':
        flux_string = 'foreign trade'
    elif flow == 'import_value':
        flux_string = ' import'
    elif flow == 'export_value':
        flux_string = 'export'
    else:
        flux_string = 'trade balance (surplus)'

    title = "Top {} countries for the year {} and category {}, serbian {}".format(num, year, category, flux_string)
   
    return {"data": data,
            'layout': {
                'title': title,
                'colorway':["#4f9da6", "#facf5a","#ff5959","#930077","#233142"],
                 'height':700
            }
            }



@app.callback(
    Output(component_id='map-graph', component_property='figure'),
    [Input(component_id='category-map', component_property='value'),
    Input(component_id='flow-map', component_property = 'value'),
    Input(component_id='year-map', component_property='value'),]
)
def update_map(category, flow, year):


    if category ==None:
        category ='All'


    m = data_mapper(category=category, flux = flow, year = year)

    #m['ccode'] = m['ccode'].map(convert_ccode)

    if flow=='export_value':
        title = 'Serbian export  / {} / {}'.format(category, year)
    elif flow=='import_value':
        title = 'Serbian import / {} / {}'.format(category, year)
    elif flow=='exchange':
        title = 'Serbian trade / {} / {}'.format(category, year)
    else:
        title = 'Serbian trade balance / {} / {}'.format(category, year)


    map_data = [go.Choropleth(
        locations = m['ccode'],
        z = m[flow],
        text = m['country'],
        colorscale=[[0.0, 'rgb(165,0,38)'], [0.1111111111111111, 'rgb(215,48,39)'], [0.2222222222222222, 'rgb(244,109,67)'],
            [0.3333333333333333, 'rgb(253,174,97)'], [0.4444444444444444, 'rgb(254,224,144)'], [0.5555555555555556, 'rgb(224,243,248)'],
            [0.6666666666666666, 'rgb(171,217,233)'],[0.7777777777777778, 'rgb(116,173,209)'], [0.8888888888888888, 'rgb(69,117,180)'],
            [1.0, 'rgb(49,54,149)']],
        #colorscale = 'YlGnBu',
        autocolorscale = False,
        reversescale = False,
        marker = go.choropleth.Marker(
            line = go.choropleth.marker.Line(
                color = 'rgb(180,180,180)',
                width = 0.5
            )),
        colorbar = go.choropleth.ColorBar(
            tickprefix = '$',
            title = 'Trade<br>Thousands US$'),
    )]

    map_layout = go.Layout(
        title = go.layout.Title(
            text = title            
        ),
        height=800,
        geo = go.layout.Geo(
            showframe = False,
            showcoastlines = False,
            projection = go.layout.geo.Projection(
                type = 'equirectangular'
            )
        ),
        annotations = [go.layout.Annotation(
            x = 0.55,
            y = 0.1,
            xref = 'paper',
            yref = 'paper',
            text = 'Source: <a href="http://www.stat.gov.rs/">\
            Statistical Office of The Republic Of Serbia</a>',
            showarrow = False
        )]
    )

    return {"data": map_data,
            'layout': map_layout
            }





@app.callback(
    Output(component_id='drilldown-graph-2', component_property='figure'),
    [Input(component_id='country-drilldown-selector', component_property='value'),
    Input(component_id='drilldown-slider-2', component_property='value'),
    Input(component_id='flow-drilldown-selector-2', component_property = 'value'),
    Input(component_id='drilldown-year-slider-2', component_property='value'),]
)
def update_country_drilldown(country, num ,flow, year):


    if country ==None:
        country ='All'

    topN = top_N_sectors(N=num, year=year, flux=flow, country=country)

  



    data=[
               {
                "values": topN.values,
                "labels": topN.index,
                "domain": {"column": 0},
                "name": "Top N",
                "hoverinfo":"label+value+name",
                "hole": .5,
                "type": "pie"
                }]
    
    if flow == 'exchange':
        flux_string = 'foreign trade'
    elif flow == 'import_value':
        flux_string = 'serbian import'
    elif flow == 'export_value':
        flux_string = 'serbian export'
    else:
        flux_string = 'trade balance (surplus)'

    title = "Top {} categories for the year {} and country {}, {}".format(num, year, country, flux_string)
   
    return {"data": data,
            'layout': {
                'title': title,
                'colorway':["#4f9da6", "#facf5a","#ff5959","#930077","#233142"],
                 'legend':{"x": 0, "y": 0, "orientation": "h"},
                 'height':700
            }
            }


if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')