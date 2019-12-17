import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
from apps.dashtest.models import DashSimpleModel
from django.db import connection

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='WebsocketExample')   # replaces dash.Dash

# get new layout when reloading the page
def serve_layout():
    # get data
    query = str(DashSimpleModel.objects.all().query)
    df = pd.read_sql_query(query, connection)

    return html.Div(id='main',
                    children=[
    dcc.Graph(
        id='live-graph',
        figure={
            'data': [{
                'x': df['x'], 
                'y': df['y'], 
                'name': 'data points',
                'mode': 'markers',
                'marker': {'size': 12}
                },
                {
                'x': [2,4],
                'y': [20,20],
                'name': 'therapy with line',
                'mode': 'lines',
                'marker': {'size': 30},
                'line': {'width': 30}
                }
            ],
            'layout': {
                'title': 'Dash Live Update via Websocket',
                'xaxis':{
                    'title':'days'
                },
                'yaxis': {
                    'title':'parameter in unit'
                },
                'legend': {
                    'orientation':'h'
                },
            'shapes': [
                # Rectangle reference to the axes
                {
                    'type': 'rect',
                    'name': 'shape',
                    'xref': 'x',
                    'yref': 'y',
                    'x0': 2.5,
                    'y0': 0,
                    'x1': 3.5,
                    'y1': 2,
                    'line': {
                        'color': 'rgb(55, 128, 191)',
                        'width': 3,
                    },
                    'fillcolor': 'rgba(55, 128, 191, 0.6)',
                },
                # Rectangle reference to the plot
                {
                    'type': 'rect',
                    'xref': 'x',
                    'yref': 'paper',
                    'x0': 0.25,
                    'y0': 0,
                    'x1': 0.5,
                    'y1': 0.5,
                    'line': {
                        'color': 'rgb(50, 171, 96)',
                        'width': 3,
                    },
                    'fillcolor': 'rgba(50, 171, 96, 0.6)',
                },
            ]

            }
        }
    )

]) # end of 'main

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)