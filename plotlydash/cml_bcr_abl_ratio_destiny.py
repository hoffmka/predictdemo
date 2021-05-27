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
import pandas as pd
import requests

from django.db import connections

from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash(name='CML_BCR-ABL-Ratio-Destiny', id='targetId')

app.layout = html.Div(id= 'main',
                    children=[
                        dcc.Input(id='targetId', value='initial value', type='hidden'),
                        html.Div(id = 'check_div',
                            style={'align': 'center'},
                            children=[
                                html.P('Select plot:'),
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=[
                                        {'label': 'all', 'value': 'graph1'}
                                    ],
                                    value='graph1'
                                ),
                            ]),
                        dcc.Graph(id='live-graph'),
                        #html.Div(id='display'),  #To show format of selectData
                    ])

@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    [Input(component_id='targetId', component_property='value'),
    Input(component_id='dropdown', component_property='value')])
def execute_query(targetId_value, dropdown_value):
    # get BCR-ABL/ABL values
    diagnostic = Diagnostic.objects.filter(targetId__startswith='demo_destiny', diagType_id = 1)
    diag_pivot = pivot(diagnostic, ['targetId', 'sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
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
    df.loc[df['BCR-ABL/ABL'] == 0, 'lratio'] = -4 # 'lql' = np.log10(3 / df.loc[df['BCR-ABL/ABL'] == 0, 'ABL'] * 100)

    #get treatments
    # treatment = TreatMedication.objects.filter(targetId__startswith='demo_nordcml006')
    # if treatment.exists():
    #     treat = treatment.values('targetId', 'dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit','medScheme')
    #     dfmedi = pd.DataFrame.from_records(data = treat)
    #     # Replace dateEnd of treatment with last sampledate, if dateEnd doesn't exist.
    #     dfmedi['dateEnd'].replace(to_replace=[None], value=df['sampleDate'].max(), inplace=True)

    # df = df.merge(dfmedi, on = 'targetId')

    # if dropdown_value == 'graph1':
    #     df = df
    # elif dropdown_value == 'graph2':
    #     df = df[df['drugName']=='Imatinib']
    # elif dropdown_value == 'graph3':
    #     df = df[df['drugName']=='Dasatinib']

    # update graphic
    # graph_figure = {
    #     'data': [{
    #         'x': df['sampleDate'], 
    #         'y': df['lratio'], 
    #         'line_group': df['targetId'],
    #         'name': 'detected BCR-ABL value',
    #         'mode': 'markers+lines',
    #         #'marker': {'size': 12, 'color': 'rgb(0, 102, 204)'},
    #         'color': df['targetId'],
    #         'text': df['BCR-ABL/ABL'],
    #         'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
    #             '<b>BCR-ABL/ABL Ratio: %{text}</b><br>'
    #         },
            # {
            # 'x': df['sampleDate'],
            # 'y': df['lql'],
            # 'name': 'negative measurement; triangle indicates estimated quantification limit',
            # 'mode': 'markers',
            # 'marker': {'size': 12, 'symbol': 'triangle-down', 'color': 'rgb(0, 102, 204)'},
            # 'text': df['ABL'],
            # 'hovertemplate': '%{xaxis.title.text}: %{x}<br>' + 
            #     '<b>BCR-ABL/ABL Ratio: 0</b><br>' +
            #     'ABL Numbers: %{text}'
            # },
            # {
            # 'x': dfmedi['dateBegin'],
            # 'y': [1.5, 1.5],
            # 'mode': 'text',
            # 'text': dfmedi['interval'].astype(str) + ' x ' + dfmedi['dosage'].astype(str) + ' ' + dfmedi['dosageUnit'] + '<br>' + dfmedi['drugName'],
            # 'textposition': 'bottom right',
            # 'showlegend': False
            # }
    #     ],
    #     'layout': {
    #         'title': 'BCR-ABL/ABL Monitoring',
    #         'xaxis':{
    #             'title':'Date',
    #             'hoverformat': '%Y-%m-%d',
    #             'gridcolor': '#E0E0E0'
    #         },
    #         'yaxis': {
    #             'title':'BCR-ABL/ABL',
    #             'tickvals': [2, 1, 0, -1, -2, -3], 
    #             'ticktext': ['100 %', '10 %', '1 %', 'MR3<br>(0.1 %)', 'MR4<br>(0.01 %)', 'MR5<br>(0.001 %)'],
    #             'zeroline': False,
    #             'gridcolor': '#E0E0E0'
    #         },
    #         'legend': {
    #             #'orientation':'h'
    #             'xanchor':"center",
    #             'yanchor':"top",
    #             'y':-0.3, #play with it
    #             'x':0.5   #play with it
    #         },
    #     }
    # }

    # Adding therapy as shape

    # if treatment.exists():
    #     graph_figure['layout']['shapes'] = []

    #     shape_1 =   {
    #         'type': 'rect',
    #         'xref': 'x',
    #         'yref': 'paper',
    #         'x0': dfmedi['dateBegin'].astype(str).tolist()[0],
    #         'y0': 0,
    #         'x1': dfmedi['dateEnd'].astype(str).tolist()[0],
    #         'y1': 1,
    #         'line': {
    #             'color': 'rgb(255, 255, 204)',
    #             'width': 1,
    #         },
    #         'fillcolor': 'rgb(255, 255, 204)',
    #         'layer': 'below',
    #     }

        # shape_2 =   {
        #     'type': 'rect',
        #     'xref': 'x',
        #     'yref': 'paper',
        #     'x0': dfmedi['dateBegin'].astype(str).tolist()[1],
        #     'y0': 0,
        #     'x1': dfmedi['dateEnd'].astype(str).tolist()[1],
        #     'y1': 1,
        #     'line': {
        #         'color': 'rgb(255, 204, 153)',
        #         'width': 1,
        #     },
        #     'fillcolor': 'rgb(255, 204, 153)',
        #     'layer': 'below',
        # }
        
    # graph_figure['layout']['shapes'].append(shape_1)
    # graph_figure['layout']['shapes'].append(shape_2)
    # graph_figure = px.line(df, 
    #     x="sampleDate", 
    #     y="lratio", 
    #     color="targetId",
    #     line_group="targetId", 
    #     hover_name="targetId")

    # graph_figure.update_traces(
    #     mode='lines+markers',
        
    # )titanic[titanic["Age"] > 35]

    #create patient_list
    df_pat = pd.DataFrame(df['targetId'].unique(), columns=['targetId'])
    # default visibility of trace
    df_pat['visible'] = 'legendonly'
    df_pat.iloc[::5,1] = True

    graph_figure = go.Figure()

    for patient in df['targetId'].unique():
        df1 = df[df["targetId"] == patient]
        df1['time'] = ((df1['sampleDate']-df1['sampleDate'].min())/np.timedelta64(1, 'M'))
        df1 = df1.sort_values(by='time')
        #df1['time'] = df1['time'].round(0).astype(int)
        #treatment = TreatMedication.objects.filter(targetId=patient)
        color = 'orange'
        # if treatment.exists():
        #     treat = treatment.values('targetId', 'dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit','medScheme')
        #     dfmedi = pd.DataFrame.from_records(data = treat)
        #     # Replace dateEnd of treatment with last sampledate, if dateEnd doesn't exist.
        #     dfmedi['dateEnd'].replace(to_replace=[None], value=df['sampleDate'].max(), inplace=True)
        #     if (dfmedi['drugName'][0]=='Imatinib'): 
        #         color = 'blue'
        #     elif (dfmedi['drugName'][0]=='Dasatinib'):
        #         color = 'red'
        
        # default visibility of trace
        if df_pat[df_pat['targetId']==patient]['visible'].values[0] == 'legendonly':
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

    # graph_figure.add_trace(go.Scatter(
    #                 x=[30], 
    #                 y=[2.5],
    #                 text=['- Nilotinib'],
    #                 mode='text',
    #                 textfont= {'color':['green']}, 
    #                 textposition= 'bottom right',
    #                 showlegend= False
    #                 ))

    graph_figure.update_layout(
        title='BCR-ABL/ABL Monitoring',
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