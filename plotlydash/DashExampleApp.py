import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import pandas as pd
from django.db import connection, connections

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='WebsocketExample', id='prediction_id')   # replaces dash.Dash

# get new layout when reloading the page
def serve_layout():
    # get data from djangoModel
    #query = str(DashSimpleModel.objects.all().query)
    #df = pd.read_sql_query(query, connection)

    with connections['HaematoOPT'].cursor() as cursor:
        query1 = "SELECT * FROM udv_PredictDemo_BCRABLratio_V where pid = 'mdat_078755'"
        cursor.execute(query1)
        results = cursor.fetchall()
        df = pd.DataFrame(results)

    return html.Div(id='main',
                    children=[
                        dcc.Input(id='prediction_id', value='initial value'),
                        html.Div(id='div'),
    dcc.Graph(
        id='live-graph',
        figure={
            'data': [{
                'x': df[2], 
                'y': df[3], 
                'name': 'data points',
                'mode': 'markers',
                'marker': {'size': 12}
                },
                # {
                # 'x': [2,4],
                # 'y': [20,20],
                # 'name': 'therapy with line',
                # 'mode': 'lines',
                # 'marker': {'size': 30},
                # 'line': {'width': 30}
                # }
            ],
            'layout': {
                'title': 'Dash test',
                'xaxis':{
                    'title':'Date'
                },
                'yaxis': {
                    'title':'BCR-ABL/ABL'
                },
                'legend': {
                    'orientation':'h'
                },
            # 'shapes': [
            #     # Rectangle reference to the axes
            #     {
            #         'type': 'rect',
            #         'name': 'shape',
            #         'xref': 'x',
            #         'yref': 'y',
            #         'x0': 2.5,
            #         'y0': 0,
            #         'x1': 3.5,
            #         'y1': 2,
            #         'line': {
            #             'color': 'rgb(55, 128, 191)',
            #             'width': 3,
            #         },
            #         'fillcolor': 'rgba(55, 128, 191, 0.6)',
            #     },
            #     # Rectangle reference to the plot
            #     {
            #         'type': 'rect',
            #         'xref': 'x',
            #         'yref': 'paper',
            #         'x0': 0.25,
            #         'y0': 0,
            #         'x1': 0.5,
            #         'y1': 0.5,
            #         'line': {
            #             'color': 'rgb(50, 171, 96)',
            #             'width': 3,
            #         },
            #         'fillcolor': 'rgba(50, 171, 96, 0.6)',
            #     },
            # ]

            }
        }
    )

]) # end of 'main

app.layout = serve_layout

@app.callback(
    Output('div', component_property='children'),
    [Input('prediction_id', component_property='value')])
def div_update(prediction_id_value):
    return prediction_id_value

if __name__ == '__main__':
    app.run_server(debug=True)