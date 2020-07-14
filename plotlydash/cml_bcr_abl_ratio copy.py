import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly
import plotly.graph_objs as go

import math
import numpy as np
import pandas as pd
import requests

from django.db import connections

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='CML_BCR-ABL-Ratio', id='targetId')

# get new layout when reloading the page
def serve_layout():
    return html.Div(id='main',
                    children=[
                        dcc.Input(id='targetId', value='initial value', type='hidden'),
                        html.Div(id='output-query'),
                        dcc.Graph(id='live-graph')
                    ]) # end of 'main

'''@app.callback(
    Output('output-query', component_property='children'),
    [Input('targetId', component_property='value')])
def run_query(targetId_value):
    query = "SELECT * FROM udv_PredictDemo_BCRABLratio_V where pid = '%s'" % targetId_value
    return query'''

@app.callback(
    Output('live-graph', component_property='figure'),
    [Input('targetId', component_property='value')])
def execute_query(targetId_value):
    with connections['HaematoOPT'].cursor() as cursor:
        # retrieve diagnostic values 
        query = "SELECT * FROM udv_PredictDemo_BCRABLratio_V where DosePhaseSample <> 'stop' and pid = '%s'" % targetId_value
        cursor.execute(query)
        results = cursor.fetchall()
        # retrieve treatments
        queryTreat = "SELECT * FROM udv_PredictDemo_TreatDrug_V where TreatmentSchemeId <> 38 and pid = '%s'" % targetId_value
        cursor.execute(queryTreat)
        resultsTreat = cursor.fetchall()
    
    df = pd.DataFrame(results, columns = ['HOPT_PatientID', 'SampleID', 'SampleDate', 'ABL', 'BCR-ABL-Ratio', 'targetId', 'DosePhaseSample'])
    df.loc[df['BCR-ABL-Ratio'] != 0, 'det'] = 'detected value'
    df.loc[df['BCR-ABL-Ratio'] == 0, 'det'] = 'not detected value'

    df.loc[df['BCR-ABL-Ratio'] != 0, 'lratio'] = np.log10(df.loc[df['BCR-ABL-Ratio'] != 0,'BCR-ABL-Ratio'])
    df.loc[df['BCR-ABL-Ratio'] == 0, 'lql'] = np.log10(3 / df.loc[df['BCR-ABL-Ratio'] == 0, 'ABL'] * 100)

    dfTreat = pd.DataFrame(resultsTreat, columns = ['PID', 'TretmentTypeID', 'Treatment', 'TreatmentSchemeID', 'TreatmentSchemeName', 'TreatmentValueDateBegin', 'TreatmentValueDateEnd', 'Interval', 'IntervalUnit', 'DrugID', 'Name', 'Dosage', 'DosageUnit'])
    dfTreat['TreatmentValueDateBegin'] = dfTreat['TreatmentValueDateBegin'].astype(str)
    dfTreat['TreatmentValueDateEnd'] = dfTreat['TreatmentValueDateEnd'].astype(str)
    x0 = dfTreat['TreatmentValueDateBegin'].astype(str).tolist()
    x1 = dfTreat['TreatmentValueDateEnd'].astype(str).tolist()

    # update graphic
    graph_figure = {
        'data': [{
            'x': df['SampleDate'], 
            'y': df['lratio'], 
            'name': 'detected values',
            'mode': 'markers',
            'marker': {'size': 12, 'color': 'rgb(0, 102, 204)'},
            'text': df['BCR-ABL-Ratio']
            },
            {
            'x': df['SampleDate'],
            'y': df['lql'],
            'name': 'value below detection limit',
            'mode': 'markers',
            'marker': {'size': 12, 'symbol': 'triangle-down', 'color': 'rgb(0, 102, 204)'}  
            }
        ],
        'layout': {
            'title': 'BCR-ABL/ABL Monitoring',
            'xaxis':{
                'title':'Date'
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
                 # Rectangle reference to the plot
                 {
                     'type': 'rect',
                     'xref': 'x',
                     'yref': 'paper',
                     'x0': x0[0],
                     'y0': 0,
                     'x1': x1[0],
                     'y1': 1,
                     'line': {
                         'color': 'rgb(255, 153, 102)',
                         'width': 1,
                     },
                     'fillcolor': 'rgb(255, 204, 153)',
                     'layer': 'below',
                 },
                 {
                     'type': 'rect',
                     'xref': 'x',
                     'yref': 'paper',
                     'x0': x0[1],
                     'y0': 0,
                     'x1': x1[1],
                     'y1': 1,
                     'line': {
                         'color': 'rgb(255, 153, 102)',
                         'width': 1,
                     },
                     'fillcolor': 'rgb(255, 255, 204)',
                     'layer': 'below',
                 },
            ]
        }
    }

    return graph_figure


app.layout = serve_layout

if __name__ == '__main__':
    app.run_server(debug=True)