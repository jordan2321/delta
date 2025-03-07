import pandas as pd
import dash
from dash import html
from dash import dcc

import plotly.express as px
import json

class Carte():
    def __init__(self, application = None):
        self.df = pd.read_pickle('data/deces_par_departements.pkl')

        self.df_naiss = pd.read_pickle('data/naissances_par_departements.pkl')

        departements = json.load(open('data/departements-avec-outre-mer.geojson'))

        fig = px.choropleth_mapbox(self.df, geojson=departements,
                                   locations='DEP', featureidkey='properties.code',  # join keys
                                   color='deces pour 10000',
                                   hover_name='DEP_NAME',
                                   hover_data=['deces pour 10000', 'DECES', 'population'],
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 47, "lon": 2},
                                   opacity=0.5,
                                   labels={'DEP': 'Numéro du département',
                                           'deces pour 10000': 'Part des décès pour 10 000',
                                           'DECES': 'Nombre de décès',
                                           'population': 'Population du département'}
                                   )

        fig2 = px.choropleth_mapbox(self.df_naiss, geojson=departements,
                                   locations='DEP', featureidkey='properties.code',  # join keys
                                   color='Naissances pour 10000',
                                   hover_name='DEP_NAME',
                                   hover_data=['Naissances pour 10000', 'NAISSANCES', 'population'],
                                   color_continuous_scale="Viridis",
                                   mapbox_style="carto-positron",
                                   zoom=4.6, center={"lat": 47, "lon": 2},
                                   opacity=0.5,
                                   labels={'DEP': 'Numéro du département',
                                           'Naissances pour 10000': 'Part des naissances pour 10 000',
                                           'NAISSANCES': 'Nombre de naissances',
                                           'population': 'Population du département'}
                                   )


        self.main_layout = html.Div(children=[
            html.H1(children='Cartes de France 2020'),
            html.Br(),
            html.Div(children=[
                html.Div(children=[
                    html.H4(children='Carte des décès par département en France en 2020'),
                    dcc.Graph(
                        id='example-graph',
                        figure=fig
                    )
                ], style={'flex': 1}),
                html.Div(children=[
                    html.H4(children='Carte des naissances par département en France en 2020'),
                    dcc.Graph(
                        id='example-graph',
                        figure=fig2
                    )
                ], style={'flex': 1})
            ], style={
                'padding': '5',
                'display': 'flex',
                'flex-direction': 'row'}
            )
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 30px 10px 30px'
             }
        )

        if application:
            self.app = application
            # application should have its own layout and use self.main_layout as a page or in a component
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout
