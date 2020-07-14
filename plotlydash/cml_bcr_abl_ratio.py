import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from django.db.models import F, Max
from apps.dbviews.models import Diagnostic, TreatMedication
from django_pivot.pivot import pivot

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

app.layout = html.Div(id= 'main',
                    children=[
                        dcc.Input(id='targetId', value='initial value', type='hidden'),
                        dcc.Graph(id='live-graph'),
                        #html.Div(id='display'),  #To show format of selectData
                    ])

@app.callback(
    Output('live-graph', component_property='figure'),
    [Input('targetId', component_property='value')])
def execute_query(targetId_value):
    # get BCR-ABL/ABL values
    diagnostic = Diagnostic.objects.filter(targetId = targetId_value, diagType_id = 1) # diagType = PCR - BCR-ABL/ABL
    diag_pivot = pivot(diagnostic, ['sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
    df = pd.DataFrame(diag_pivot, columns = ['sampleId', 'sampleDate', 'ABL', 'BCR-ABL/ABL'])
    # prepare data for plot
    df['BCR-ABL/ABL'] = pd.to_numeric(df['BCR-ABL/ABL'])
    df['ABL'] = pd.to_numeric(df['ABL'])

    df.loc[df['BCR-ABL/ABL'] != 0, 'det'] = 'detected value'
    df.loc[df['BCR-ABL/ABL'] == 0, 'det'] = 'not detected value'

    df.loc[df['BCR-ABL/ABL'] != 0, 'lratio'] = np.log10(df.loc[df['BCR-ABL/ABL'] != 0,'BCR-ABL/ABL'])
    df.loc[df['BCR-ABL/ABL'] == 0, 'lql'] = np.log10(3 / df.loc[df['BCR-ABL/ABL'] == 0, 'ABL'] * 100)

    # get treatments
    treatment = TreatMedication.objects.filter(targetId = targetId_value)
    if treatment.exists():
        treat = treatment.values('dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit','medScheme')
        dfmedi = pd.DataFrame.from_records(data = treat)
        # Replace dateEnd of treatment with last sampledate, if dateEnd doesn't exist.
        dfmedi['dateEnd'].replace(to_replace=[None], value=df['sampleDate'].max(), inplace=True)


    # update graphic
    graph_figure = {
        'data': [{
            'x': df['sampleDate'], 
            'y': df['lratio'], 
            'name': 'detected BCR-ABL value',
            'mode': 'markers',
            'marker': {'size': 12, 'color': 'rgb(0, 102, 204)'},
            'text': df['BCR-ABL/ABL'],
            'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                '<b>BCR-ABL/ABL Ratio: %{text}</b><br>'
            },
            {
            'x': df['sampleDate'],
            'y': df['lql'],
            'name': 'negative measurement; triangle indicates estimated quantification limit',
            'mode': 'markers',
            'marker': {'size': 12, 'symbol': 'triangle-down', 'color': 'rgb(0, 102, 204)'},
            'text': df['ABL'],
            'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                '<b>BCR-ABL/ABL Ratio: 0</b><br>' +
                'ABL Numbers: %{text}'
            },
            {
            'x': dfmedi['dateBegin'],
            'y': [1.5, 1.5],
            'mode': 'text',
            'text': dfmedi['interval'].astype(str) + ' x ' + dfmedi['dosage'].astype(str) + ' ' + dfmedi['dosageUnit'] + '<br>' + dfmedi['drugName'],
            'textposition': 'bottom right',
            'showlegend': False
            }
        ],
        'layout': {
            'title': 'BCR-ABL/ABL Monitoring',
            'xaxis':{
                'title':'Date',
                'hoverformat': '%Y-%m-%d',
                'gridcolor': '#E0E0E0'
            },
            'yaxis': {
                'title':'BCR-ABL/ABL',
                'tickvals': [2, 1, 0, -1, -2, -3], 
                'ticktext': ['100 %', '10 %', '1 %', 'MR3<br>(0.1 %)', 'MR4<br>(0.01 %)', 'MR5<br>(0.001 %)'],
                'zeroline': False,
                'gridcolor': '#E0E0E0'
            },
            'legend': {
                #'orientation':'h'
                'xanchor':"center",
                'yanchor':"top",
                'y':-0.3, #play with it
                'x':0.5   #play with it
            },
        }
    }

    # Adding therapy as shape

    if treatment.exists():
        graph_figure['layout']['shapes'] = []

        shape_1 =   {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': dfmedi['dateBegin'].astype(str).tolist()[0],
            'y0': 0,
            'x1': dfmedi['dateEnd'].astype(str).tolist()[0],
            'y1': 1,
            'line': {
                'color': 'rgb(255, 255, 204)',
                'width': 1,
            },
            'fillcolor': 'rgb(255, 255, 204)',
            'layer': 'below',
        }

        shape_2 =   {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': dfmedi['dateBegin'].astype(str).tolist()[1],
            'y0': 0,
            'x1': dfmedi['dateEnd'].astype(str).tolist()[1],
            'y1': 1,
            'line': {
                'color': 'rgb(255, 204, 153)',
                'width': 1,
            },
            'fillcolor': 'rgb(255, 204, 153)',
            'layer': 'below',
        }

        
        graph_figure['layout']['shapes'].append(shape_1)
        graph_figure['layout']['shapes'].append(shape_2)
        
    return graph_figure

# Show result of selecting data with either box select or lasso
#@app.callback(Output('display','children'),[Input('live-graph','selectedData')])
#def selectData(selectData):
#    return str('Selecting points produces a nested dictionary: {}'.format(selectData))


if __name__ == '__main__':
    app.run_server(debug=True)