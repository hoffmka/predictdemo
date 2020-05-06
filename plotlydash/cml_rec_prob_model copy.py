import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from django.conf import settings
from django_plotly_dash import DjangoDash
from apps.predictions.models import Project, Prediction

import math
import numpy as np
import os
import pandas as pd

import plotly
import plotly.graph_objs as go

import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='CML_RecurranceModel', id='prediction_id')

app.layout = html.Div(id= 'main',
                    children=[
                        dcc.Input(id='prediction_id', value='initial value'),
                        dcc.Graph(
                            id='graph',
                            )
                    ])
@app.callback(
    Output('graph', component_property='figure'),
    [Input('prediction_id', component_property='value')]
)
def graph_update(prediction_id_value):
    prediction = Prediction.objects.get(id=prediction_id_value)
    magpieJobId = prediction.magpieJobId
    project_id = prediction.project_id
    project = Project.objects.get(id=project_id)
    magpieProjectId = project.magpieProjectId

    path2data = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/pat1.csv')))))))
    df = pd.read_csv(path2data, sep=';')
    
    # Deleting lql / lratio values for detected / non detected
    df.loc[df['det'] == 'detected value', 'lql'] = None
    df.loc[df['det'] == 'value below detection limit', 'lratio'] = None

    # update graph
    figure = {
        'data': [
            {
                'x': df['Sample.Date'],
                'y': df['lratio'],
                'name': 'detected BCR-ABL value',
                'mode': 'markers',
                'marker': {'size': 12, 'color': 'rgb(0, 102, 204)'},
                'text': df['BCR.ABL.Ratio'],
                'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                    '<b>BCR-ABL/ABL Ratio: %{text}</b><br>' + '<extra></extra>'
            },
            {
                'x': df['Sample.Date'],
                'y': df['lql'],
                'name': 'negative measurement; triangle indicates estimated quantification limit',
                'mode': 'markers',
                'marker': {'size': 12, 'symbol': 'triangle-down', 'color': 'rgb(0, 102, 204)'},
                'text': df['Control.Gene'],
                'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                    '<b>BCR-ABL/ABL Ratio: 0</b><br>' +
                    'ABL Numbers: %{text}<extra></extra>'
            }
        ],
        'layout': {
                'title': 'Recurrance probability after stopping',
                'xaxis': {
                    'title':'Date',
                    'hoverformat': '%Y-%m-%d'
                },
                'yaxis': {
                    'title':'BCR-ABL/ABL',
                    'tickvals': [2, 1, 0, -1, -2, -3], 
                    'ticktext': ['100 %', '10 %', '1 %', 'MR3', 'MR4', 'MR5'],
                    'zeroline': False
                },
                'legend': {
                    #'orientation':'h'
                    'xanchor':"center",
                    'yanchor':"top",
                    'y':-0.3, #play with it
                    'x':0.5   #play with it
                },
                'shapes': [
                    {
                        'type': 'rect',
                        'xref': 'x',
                        'yref': 'paper',
                        'x0': df['HalfDose.Start.Date'].astype(str).tolist()[0],
                        'y0': 0,
                        'x1': df['HalfDose.End.Date'].astype(str).tolist()[0],
                        'y1': 1,
                        'line': {
                            'color': 'rgb(255, 153, 102)',
                            'width': 1,
                     },
                        'fillcolor': 'rgb(255, 255, 204)',
                        'layer': 'below',
                    },
                    {
                        'type': 'line',
                        'x0': df['HalfDose.Start.Date'].astype(str).tolist()[0],
                        'y0': 0,
                        'x1': df['HalfDose.End.Date'].astype(str).tolist()[0],
                        'y1': 2,
                        'line': {
                            'color': 'red',
                            'width': 3,
                        },
                    }
                ]
            }  
    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)