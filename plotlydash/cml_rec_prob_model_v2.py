import dash
import dash_bootstrap_components as dbc
from dash import dcc
#import dash_html_components as html
from dash import Input, Output, html

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

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = DjangoDash(
    name='CML_RecurranceModel_V2', 
    add_bootstrap_links=True, 
    id='prediction_id')

app.layout = html.Div(
    id= 'main',
    children=[
        dcc.Input(
            id='prediction_id', 
            value='initial value', 
            type='hidden'
            ),
        dcc.Dropdown(
            id="dropdown",
            options=[
                {"label": "Expert view", "value": "expert"},
                {"label": "Simplified view", "value": "simple"},
            ],
            value='simple',
            style={"display": "none"},  # hide dropdown
        ),
        dcc.Graph(
            id='graph'
        ),
    ]
)

@app.callback(
    Output('graph', component_property='figure'),
    [Input('prediction_id', component_property='value'),
    Input('dropdown', component_property='value')],
)
def graph_update(prediction_id_value, dropdown_value):
    prediction = Prediction.objects.get(id=prediction_id_value)
    magpieJobId = prediction.magpieJobId
    project_id = prediction.project_id
    project = Project.objects.get(id=project_id)
    magpieProjectId = project.magpieProjectId

    path2data = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/patient_data_result.csv')))))))
    df = pd.read_csv(path2data, sep=',')

    path2data_medi = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/patient_treatments.csv')))))))
    dfmedi = pd.read_csv(path2data_medi, sep=',')
    dfmedi = dfmedi.sort_values(by='dateBegin')

    # Deleting lql / lratio values for detected / non detected
    df.loc[df['det'] == 'detected value', 'lql'] = None
    df.loc[df['det'] == 'value below detection limit', 'lratio'] = None

    # Recurrance probability in %
    prob = df['prob'].max()

    # CI in %
    ci_min = df['min'].max()
    ci_max = df['max'].max()

    # linear regression
    df.sort_values(by=['sampleDate'])
    time = df.loc[df['time'] >= 0, 'time']
    df['fit'] = df['slope'] * time + df['intercept']

    ###############
    # update graph
    ##############

    # expert view
    if dropdown_value == "expert":
        figure = {
            'data': [
                {
                    'x': df['sampleDate'],
                    'y': df['lratio'],
                    'name': 'detected BCR-ABL value',
                    'mode': 'markers',
                    'marker': {'size': 8, 'color': 'rgb(0, 37, 87)'},
                    'text': df['BCR.ABL.ABL'],
                    'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                        '<b>BCR-ABL/ABL Ratio: %{text}</b><br>' + '<extra></extra>'
                },
                {
                    'x': df['sampleDate'],
                    'y': df['lql'],
                    'name': 'negative measurement; triangle indicates estimated quantification limit',
                    'mode': 'markers',
                    'marker': {'size': 8, 'symbol': 'triangle-down', 'color': 'rgb(0, 37, 87)'},
                    'text': df['ABL'],
                    'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                        '<b>BCR-ABL/ABL Ratio: 0</b><br>' +
                        'ABL Numbers: %{text}<extra></extra>'
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
                    'title': 'Recurrance probability after stopping:<br><b>' + str(prob) + ' %</b><br>95%-CI:[' + str(ci_min) + '%, '+ str(ci_max) + '%]',
                    'xaxis': {
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
                    }
                }  
        }

        # Adding fit/line
        if (df['risk'].min() == 'slope during half dose period (high)'):
            line_color = '#FF0000'
        else:
            line_color = '#009900'

        line =  {
            'x': df['sampleDate'],
            'y': df['fit'],
            'mode': 'lines',
            'line': {'color': line_color, 'width': 4},
            'name': df['risk'].max(),
            'connectgaps': True,
            'hoverinfo': 'skip'
        }
        
        # Adding therapy as shape
        figure['layout']['shapes'] = []

        dfmedi_fulldose = dfmedi[dfmedi['medScheme']=='full dose']
        shape_1 =   {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': dfmedi_fulldose['dateBegin'].astype(str).tolist()[0],
            'y0': 0,
            'x1': dfmedi_fulldose['dateEnd'].astype(str).tolist()[0],
            'y1': 1,
            'line': {
                'color': 'rgb(255, 204, 153)',
                'width': 1,
            },
            'fillcolor': 'rgb(255, 204, 153)',
            'layer': 'below',
        }

        dfmedi_halfdose = dfmedi[dfmedi['medScheme']=='half dose']
        shape_2 =   {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': dfmedi['dateBegin'].astype(str).tolist()[1],
            'y0': 0,
            'x1': df.loc[df['time'] == df['HalfDose.time.max'], 'sampleDate'].astype(str).tolist()[0],
            'y1': 1,
            'line': {
                'color': 'rgba(255, 204, 153, 0.5)',
                'width': 1,
            },
            'fillcolor': 'rgba(255, 204, 153, 0.5)',
            'layer': 'below',
        }

        
        figure['layout']['shapes'].append(shape_1)
        figure['layout']['shapes'].append(shape_2)
        figure['data'].append(line)

    # Simplified view
    if dropdown_value == "simple":
        prob_rounded = 5*round(prob/5)
        ci_min_rounded = 5*round(ci_min/5)
        ci_max_rounded = 5*round(ci_max/5)

        if prob_rounded <=50:
            bar_col='green'
            ci_col='rgba(0,128,0,0.5)'
        else:
            bar_col='red'
            ci_col='rgba(255, 0, 0, 0.5)'

        figure = go.Figure(
            layout=go.Layout(
                    annotations=[
                        go.layout.Annotation(
                            text='    ',
                            align='center',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=0.36,
                            y=0,
                            bgcolor=ci_col
                        ),
                        go.layout.Annotation(
                            text='Prediction uncertainty (95% CI)',
                            align='center',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=0.5,
                            y=0,
                            font=dict(
                                size=14,
                                )
                        ),
                        go.layout.Annotation(
                            text='~'+str(prob_rounded)+'%',
                            align='center',
                            showarrow=False,
                            xref='paper',
                            yref='paper',
                            x=0.5,
                            y=0.3,
                            font=dict(
                                size=48,
                                )
                        )
                    ]
            )
        )
            
        figure.add_trace(go.Indicator(
            mode="gauge",
            title={'text': 'Recurrence probability after stopping the TKI treatment'},
            value=prob,
            #number={"prefix": "~", "suffix": "%"},
            delta={"position": "top", "reference": 100},
            domain={'x': [0, 1], 'y': [0.1,1]},
            gauge={'axis':{'range':[None, 100], 'tickfont':{'size':12}},
                'bar': {'color': bar_col},
                'steps': [
                    {'range': [ci_min, ci_max], 'color': ci_col}],
                'threshold' : {'line': {'color': "darkred", 'width': 4}, 'thickness': 0.75, 'value': 50}
            }
        ))
        
        figure.update_layout(showlegend=True)

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)