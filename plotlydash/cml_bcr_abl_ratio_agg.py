import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from django.db.models import F, Max, Q
from apps.dbviews.models import Diagnostic, TreatMedication
from django_pivot.pivot import pivot

import plotly
import plotly.express as px
import plotly.graph_objs as go

import math
import numpy as np
import os
import pandas as pd
import requests
import subprocess
import sys
import tempfile

from io import StringIO

from django.db import connections

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='CML_BCR-ABL-Ratio-agg', id='trial')

app.layout = html.Div(id= 'main',
                    children=[
                        dcc.Input(id='trial', value='initial value'), #, type='hidden'
                        html.Div(id = 'check_div',
                            style={'align': 'center'},
                            children=[
                                html.P('Select plot:'),
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=[
                                        {'label': 'Median and interquartile range only', 'value': 'graph1'},
                                        {'label': 'add diagnostics to legends', 'value': 'graph2'},
                                        {'label': 'show all diagnostics', 'value': 'graph3'},
                                    ],
                                    value='graph1'
                                ),
                            ]),
                        dcc.Graph(id='live-graph'),
                        #html.Div(id='display'),  #To show format of selectData
                    ])

@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    [Input(component_id='trial', component_property='value'),
    Input(component_id='dropdown', component_property='value')])
def execute_query(trial_value, dropdown_value):
    # get BCR-ABL/ABL values
    #diagnostic = Diagnostic.objects.filter(targetId__startswith='demo_nordcml006', diagType_id = 1) # diagType = PCR - BCR-ABL/ABL
    diagnostic = Diagnostic.objects.filter(trial=trial_value, diagType_id = 1)
    diag_pivot = pivot(diagnostic, ['trial', 'targetId', 'sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
    df = pd.DataFrame(diag_pivot, columns = ['targetId', 'sampleId', 'sampleDate', 'ABL', 'BCR-ABL/ABL'])
    # prepare data for plot
    df['BCR-ABL/ABL'] = df['BCR-ABL/ABL'].replace('Missing data',np.NaN)
    df['BCR-ABL/ABL'] = pd.to_numeric(df['BCR-ABL/ABL'].replace(',','.', regex=True))
    df = df.replace('NA',np.NaN)
    df['ABL'] = pd.to_numeric(df['ABL'].replace(',','.', regex=True))

    df.loc[df['BCR-ABL/ABL'] != 0, 'det'] = 'detected value'
    df.loc[df['BCR-ABL/ABL'] == 0, 'det'] = 'not detected value'
    df.loc[df['BCR-ABL/ABL'] != 0, 'marker'] = 'circle'
    df.loc[df['BCR-ABL/ABL'] == 0, 'marker'] = 'triangle-down'

    df.loc[df['BCR-ABL/ABL'] != 0, 'lratio'] = np.log10(df.loc[df['BCR-ABL/ABL'] != 0,'BCR-ABL/ABL'])
    # BEGIN for R-Script "Median-calculation"
    df['PatID'] = df['targetId']
    df['LRATIO'] = df['lratio']
    if any(pd.notnull(df['ABL'])):
        df.loc[df['BCR-ABL/ABL'] == 0, 'lQL'] = np.log10(3 / df.loc[df['BCR-ABL/ABL'] == 0, 'ABL'] * 100)
        df.loc[df['BCR-ABL/ABL'] == 0, 'lratio'] = np.log10(3 / df.loc[df['BCR-ABL/ABL'] == 0, 'ABL'] * 100)
    else:
        df.loc[df['BCR-ABL/ABL'] == 0, 'lQL'] = -2.5
        df.loc[df['BCR-ABL/ABL'] == 0, 'lratio'] = -2.5

    df.loc[df['BCR-ABL/ABL'] != 0, 'ND'] = False
    df.loc[df['BCR-ABL/ABL'] == 0, 'ND'] = True 
    # END for R-Script "Median-calculation"

    #get treatments
    treatment = TreatMedication.objects.filter(trial=trial_value)
    if treatment.exists():
        treat = treatment.values('targetId', 'dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit','medScheme')
        dfmedi = pd.DataFrame.from_records(data = treat)
        df = df.merge(dfmedi, on = 'targetId')
        '''
        if dropdown_value == 'graph1':
            df = df
        elif dropdown_value == 'graph2':
            df = df[df['drugName']=='Imatinib']
        elif dropdown_value == 'graph3':
            df = df[df['drugName']=='Dasatinib']
        '''
        # for R-Script "Median-calculation" again begin
        df['TIME'] = (df['sampleDate']-df['dateBegin']) / np.timedelta64(1, 'M')
    else:
        df_sampleDateMin = df.groupby('targetId').agg({'sampleDate': 'min'}).reset_index()
        df = df.merge(df_sampleDateMin, on = 'targetId')
        df['TIME'] = (df['sampleDate_x']-df['sampleDate_y']) / np.timedelta64(1, 'M')
    
    df = df.sort_values(by=['PatID','TIME'])
    data_Rinput = df[['PatID', 'TIME', 'LRATIO', 'lQL','ND']].copy() 
    
    #  for R-Script "Median-calculation"
    ####################################
    # create tempfile
    tf = tempfile.NamedTemporaryFile(suffix='.csv', dir='/usr/local/www/djangoprojects/predictDemo/media/documents/predictions/', delete=False)
    data_in = data_Rinput.to_csv(tf.name, sep=';', na_rep='Nan',index=False)

    args = [tf.name]
    command = 'Rscript'
    path2script = "/usr/local/www/djangoprojects/predictDemo/plotlydash/medianCalculations.R"
    #path2script = os.path.join(os.path.dirname(__file__), 'medianCalculations.R')
    cmd = [command, path2script] + args

    x = None
    try:
        x = subprocess.check_output(cmd, universal_newlines = True)
    except subprocess.CalledProcessError as e:
        x = e.output

    if x!='\n':
        df_median = pd.read_csv(StringIO(x), sep=",")
    
    os.remove(tf.name)
    # end for R-Script calculation

    # graph
    graph_figure = go.Figure()

    if dropdown_value != 'graph1':
        patlist = sorted(df['targetId'].unique())
        for patient in patlist:
            df1 = df[df["targetId"] == patient]
            df1['time'] = df1['TIME'].round(0).astype(int)
            df1 = df1.sort_values(by='time')
            #treatment = TreatMedication.objects.filter(targetId=patient)
            color = 'blue'
            # if treatment.exists():
            #     treat = treatment.values('targetId', 'dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit','medScheme')
            #     dfmedi = pd.DataFrame.from_records(data = treat)
            #     # Replace dateEnd of treatment with last sampledate, if dateEnd doesn't exist.
            #     dfmedi['dateEnd'].replace(to_replace=[None], value=df['sampleDate'].max(), inplace=True)
            #     if (dfmedi['drugName'][0]=='Imatinib'): 
            #         color = 'blue'
            #     elif (dfmedi['drugName'][0]=='Dasatinib'):
            #         color = 'red'
            #     else:
            #         color = 'grey'
            if dropdown_value == 'graph2':
                visible = 'legendonly'
            else:
                visible = True

            graph_figure.add_trace(go.Scatter(
                x=df1['time'], 
                y=df1['lratio'],
                name=patient,
                mode='lines+markers', 
                line={'color':color}, 
                marker= {'size': 12, 'symbol':df1['marker']},
                visible=visible
                #legendgroup=dfmedi['drugName'][0]
                ))

    if x!='\n':
        # add 75.Quantil
        graph_figure.add_trace(go.Scatter(
            x=df_median['Time'],
            y=df_median['Quantile75'],
            line={'color':'grey', 'width': 2},
            showlegend=False,
            name='Quantile75',
        ))
        # add 25. Quantil
        graph_figure.add_trace(go.Scatter(
            x=df_median['Time'],
        y=df_median['Quantile25'],
        name='interquartile range',
        mode='lines',
        line={'color':'grey', 'width': 2},
        fill='tonexty',
        fillcolor='rgba(0,100,80,0.6)'
        ))
        # add median
        graph_figure.add_trace(go.Scatter(
            x=df_median['Time'],
            y=df_median['Median'],
            name='median',
            mode='lines', 
            line={'color':'black', 'width': 3}, 
        ))

    # graph_figure.add_trace(go.Scatter(
    #                 x=[30, 30], 
    #                 y=[2.5, 2],
    #                 text=['- Imatinib', '- DasatinibX'],
    #                 mode='text',
    #                 textfont= {'color':['blue', 'red']}, 
    #                 textposition= 'bottom right',
    #                 showlegend= False
    #                 ))

    graph_figure.update_layout(
        title='BCR-ABL/ABL Aggregation',
        xaxis={
            'title':'Month',
            #'hoverformat': '%Y-%m-%d',
            'gridcolor': '#E0E0E0'
        },
        yaxis={
            'title':'BCR-ABL/ABL',
            'tickvals': [2, 1, 0, -1, -2, -3], 
            'ticktext': ['100 %', '10 %', '1 %', 'MR3<br>(0.1 %)', 'MR4<br>(0.01 %)', 'MR5<br>(0.001 %)'],
            'zeroline': False,
            'gridcolor': '#E0E0E0'
        }#,
        # legend={
        #     #'orientation':'h'
        #     'xanchor':"center",
        #     'yanchor':"top",
        #     'y':-0.3, #play with it
        #     'x':0.5   #play with it
        # },
    )
    
    return graph_figure

# Show result of selecting data with either box select or lasso
#@app.callback(Output('display','children'),[Input('live-graph','selectedData')])
#def selectData(selectData):
#    return str('Selecting points produces a nested dictionary: {}'.format(selectData))


if __name__ == '__main__':
    app.run_server(debug=True)