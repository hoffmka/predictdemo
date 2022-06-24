import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from django.conf import settings
from django_plotly_dash import DjangoDash
from apps.predictions.models import Project, Prediction

from datetime import datetime
import math
import numpy as np
import os
import pandas as pd

import plotly
import plotly.graph_objs as go

import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='CML_PhasePortrait', id='prediction_id')

app.layout = html.Div(id= 'main',
                    children=[
                        dcc.Input(id='prediction_id', value='initial value', type='hidden'),
                        html.Div(id = 'check_div',
                                style={'align': 'center'}),
                                dcc.Dropdown(
                                    id="dropdown",
                                    options=[
                                        {"label": "Expert view", "value": "expert"},
                                        {"label": "Simplified view", "value": "simple"},
                                    ],
                                    value="expert"
                                ),
                        dcc.Graph(id='graph'),
                    ])
@app.callback(
    Output('graph', component_property='figure'),
    [Input('prediction_id', component_property='value'),
    Input("dropdown", component_property="value")]
)
def graph_update(prediction_id_value, dropdown_value):
    prediction = Prediction.objects.get(id=prediction_id_value)
    magpieJobId = prediction.magpieJobId
    project_id = prediction.project_id
    project = Project.objects.get(id=project_id)
    magpieProjectId = project.magpieProjectId

    path2data = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/patdata_res.csv')))))))
    df = pd.read_csv(path2data, sep=',')

    path2data_medi = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/patdata_medi.csv')))))))
    dfmedi = pd.read_csv(path2data_medi, sep=';')

    path2data_sim = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/sim.csv')))))))
    dfsim = pd.read_csv(path2data_sim, sep=',')

    path2data_immunWin = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/immuneWindowRange.csv')))))))
    dfimmunWin = pd.read_csv(path2data_immunWin, sep=',')

    path2data_class = os.path.join(settings.PROJECT_DIR, os.path.join('media/documents/predictions/', os.path.join(str(prediction_id_value), os.path.join('projects', os.path.join(str(magpieProjectId), os.path.join('jobs', os.path.join(str(magpieJobId), 'results/PatientClasses.csv')))))))
    dfclass = pd.read_csv(path2data_class, sep=',', header=None)

    # Deleting lql / lratio values for detected / non detected
    df.loc[df['det'] == 'detected value', 'lQL'] = None
    df.loc[df['det'] == 'value below detection limit', 'LRATIO'] = None

    # Updating time for therapy
    dfmedi = dfmedi.sort_values(by='dateBegin')
    dfmedi.dateEnd = pd.to_datetime(dfmedi.dateEnd)
    dfmedi.dateBegin = pd.to_datetime(dfmedi.dateBegin)
    dfmedi['timeBegin'] = ((dfmedi.dateBegin-min(dfmedi.dateBegin))/np.timedelta64(1, 'M'))
    dfmedi['timeEnd'] = ((dfmedi.dateEnd-min(dfmedi.dateBegin))/np.timedelta64(1, 'M'))

    # sim Z
    for fitcount in range(1,len(dfclass)+1):
        dfsim['X'+str(fitcount)+'.logZ'] = np.log10(dfsim['X'+str(fitcount)+'.Z'])
        fitcount=fitcount+1

    # mean LRATIO
    dfsim['lratio_mean'] = np.mean(dfsim.filter(regex='LRATIO'), axis=1)
    dfsim['lratio_std'] = np.std(dfsim.filter(regex='LRATIO'), axis=1)

    # mean Z
    dfsim['logZ_mean']=np.mean(dfsim.filter(regex='logZ'),axis=1)
    dfsim['logZ_std']=np.std(dfsim.filter(regex='logZ'),axis=1)

    #immune window
    immune_window_y_min = dfimmunWin[0:int(len(dfclass)/2)].mean()['LRATIO']
    immune_window_y_max = dfimmunWin[(int(len(dfclass)/2)):int(len(dfclass))].mean()['LRATIO']

    # proportion of classes
    df_class_rep = dfclass.groupby(2, as_index=True)[2].count().reset_index(name="count")
    df_class_rep.columns = ['group', 'count']

    try: 
        df_class_rep.loc[df_class_rep.group=='A', 'count'].values[0]
    except:
        df_class_rep = df_class_rep.append({'group': 'A', 'count': 0}, ignore_index=True)

    try: 
        df_class_rep.loc[df_class_rep.group=='B', 'count'].values[0]
    except:
        df_class_rep = df_class_rep.append({'group': 'B', 'count': 0}, ignore_index=True)

    try: 
        df_class_rep.loc[df_class_rep.group=='C', 'count'].values[0]
    except:
        df_class_rep = df_class_rep.append({'group': 'C', 'count': 0}, ignore_index=True)

    df_class_rep.loc[df_class_rep.group=='A', 'description'] = 'A … insufficient immune response (TKI stop not suggested)'
    df_class_rep.loc[df_class_rep.group=='B', 'description'] = 'B … sufficient immune response (TKI stop possible after achieving sustained molecular remission)'
    df_class_rep.loc[df_class_rep.group=='C', 'description'] = 'C … weak immune response (TKI stop not suggested)'
    df_class_rep = df_class_rep.sort_values('group')
    ###############
    # update graph
    ###############

    #expert view
    if dropdown_value == "expert":
        figure = {
            'data': [
                {
                    'x': df['sampleDate'],
                    'y': df['LRATIO'],
                    'name': 'detected BCR-ABL value',
                    'mode': 'markers',
                    'marker': {'size': 8, 'color': 'rgb(0, 102, 204)'},
                    'text': df['BCR.ABL.ABL'],
                    'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
                        '<b>BCR-ABL/ABL Ratio: %{text}</b><br>' + '<extra></extra>',
                },
                {
                    'x': df['sampleDate'],
                    'y': df['lQL'],
                    'name': 'negative measurement; triangle indicates estimated quantification limit',
                    'mode': 'markers',
                    'marker': {'size': 8, 'symbol': 'triangle-down', 'color': 'rgb(0, 102, 204)'},
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
                },
                {
                    'x': [30],
                    'y': [2],
                    'xaxis': 'x2',
                    'mode': 'text',
                    'text': '<b>Patient classification (with '+ str(len(dfclass)) +' fits):</b><br />'+str(round(df_class_rep.loc[df_class_rep.group=='A', 'count'].values[0]/len(dfclass)*100))+' % in immune class A <br />'+str(round(df_class_rep.loc[df_class_rep.group=='B', 'count'].values[0]/len(dfclass)*100))+' % in immune class B<br />'+str(round(df_class_rep.loc[df_class_rep.group=='C', 'count'].values[0]/len(dfclass)*100))+' % in immune class C',
                    'textposition': 'bottom right',
                    'showlegend': False
                }                       
            ],
            'layout': {
                    'title': {
                        'text': 'Model-predicted immune classification',
                        'xanchor': 'center',
                        'yanchor': 'top',
                        #'y': -0.7,
                    },
                    'xaxis': {
                        'title':'Date',
                        'hoverformat': '%Y-%m-%d',
                        'gridcolor': '#E0E0E0',
                        'range': [(pd.to_datetime(dfmedi['dateBegin']).min() - pd.DateOffset(months=1)).strftime("%Y-%m-%d"),(pd.to_datetime(df['sampleDate']).max() + pd.DateOffset(months=6)).strftime("%Y-%m-%d")],
                        #'zeroline': False,
                    },
                    'xaxis2': {
                        'title': 'Time [month]',
                        'overlaying': 'x1',
                        'side': 'top',
                        'range': [-1, df['TIME'].max()+6],

                    },
                    'yaxis': {
                        'title':'BCR-ABL/ABL',
                        'tickvals': [2, 1, 0, -1, -2, -3], 
                        'ticktext': ['100 %', '10 %', '1 %', 'MR3<br>(0.1 %)', 'MR4<br>(0.01 %)', 'MR5<br>(0.001 %)'],
                        'zeroline': False,
                        'gridcolor': '#E0E0E0'
                    },
                    'yaxis2': {
                        'title': 'log10(Z)',
                        'range': [2, 6],
                        #'tickvals': [1, -1, -3], 
                        #'ticktext': [6, 4, 2],
                        'overlaying': 'y',
                        'side': 'right'
                    },
                    'legend': {
                        #'orientation':'h'
                        'xanchor':"center",
                        'yanchor':"top",
                        'y':-0.3, #play with it
                        'x':0.5   #play with it
                    },
                    'height': 600,
                    'margin': {
                        't': 150
                    }
                }  
        }
        
        # Adding therapy as shape

        figure['layout']['shapes'] = []

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

        figure['layout']['shapes'].append(shape_1)
        figure['layout']['shapes'].append(shape_2)

        mean_lratio = {
            'x': dfsim['X1.TIME'],
            'y': dfsim['lratio_mean'],
            'xaxis': 'x2',
            'name': 'Mean cancer cells',
            'mode': 'line',
            'line': {
                'color': 'rgb(230, 68, 46)',
            }
        }
        mean_z = {
            'x': dfsim['X1.TIME'],
            'y': dfsim['logZ_mean'],
            'xaxis': 'x2',
            'name': 'Mean immune cells',
            'mode': 'line',
            'yaxis': 'y2',
            'line': {
                'color': 'rgb(230, 68, 46)',
                'dash': 'dot'
            }
        }
        immunewin =   {
            'type': 'rect',
            'xref': 'x2',
            'yref': 'y',
            'x0': 0,
            'y0': immune_window_y_min,
            'x1': dfsim['X1.TIME'].max(),
            'y1': immune_window_y_max,
            'line': {
                'color': 'rgb(211,211,211)',
                'width': 1,
            },
            'fillcolor': 'rgba(112,128,144, 0.2)',
            'layer': 'above',
        }

        immunewin_txt =  {
                    'x': [0.5],
                    'y': [immune_window_y_max],
                    'xaxis': 'x2',
                    'mode': 'text',
                    'text': 'Immune window',
                    'textposition': 'bottom right',
                    'showlegend': False
        }

        figure['data'].append(mean_lratio)
        figure['data'].append(mean_z)
        figure['layout']['shapes'].append(immunewin)
        figure['data'].append(immunewin_txt)

    # Simplified view
    if dropdown_value == "simple":
        trace = go.Pie(
                    labels = df_class_rep['description'], 
                    values = df_class_rep['count'],
                    hole=.3,
                    marker={'colors':['red', 'green', 'grey']},
                    sort= False,
                    textfont={'color': '#FFFFFF', 'size': 20},
                    )
        data = [trace]
        figure = go.Figure(data = data)
        figure.update_layout(
                    title={
                        'text':'Model-predicted immune classification',
                        'xanchor': 'left',
	                    'yanchor': 'bottom',
	                    'xref': 'paper',
                        #'x':0.5
                        },
                    legend={
                        #'orientation':'h'
                        'xanchor':"center",
                        'yanchor':"top",
                        'y':-0.3, #play with it
                        'x':0.5   #play with it
                        }
                    )
    
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)