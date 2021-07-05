import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output

from django.contrib.auth.models import User
from django.db.models import F, Max, Q
from django_pivot.pivot import pivot

from apps.dbviews.models import PatientTrial, Diagnostic, TreatMedication
from apps.trials.models import Trial
from operator import itemgetter
from rolepermissions.checkers import has_object_permission


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
                        dcc.Input(id='trial', value='initial value', type='hidden'),
                        dcc.Input(id='user', value='initial value', type='hidden'),
                        # dropdown
                        html.Div(id = 'check_div',
                            style={'align': 'center'},
                            children=[
                                html.P('Select plot:'),
                                dcc.Dropdown(
                                    id='dropdown',
                                    options=[
                                        {'label': 'Median and interquartile range (without patient-specific time cources)', 'value': 'graph1'},
                                        {'label': 'Median and interquartile range (with disabled patient-specific time cources)', 'value': 'graph2'},
                                        {'label': 'Median and interquartile range (with patient-specific time cources)', 'value': 'graph3'},
                                    ],
                                    value='graph2'
                                )
                            ]),
                        # graph
                        dcc.Loading(
                            id="loading-1",
                            type="default",
                            children=dcc.Graph(id='live-graph')
                        ),
                        # checkbox gender
                        html.Div(id='div_properties',
                            style={'align': 'center'},
                            children=[
                                html.H4('Select gender:'),
                                dcc.Checklist(
                                    id='check_gender',
                                    options = [
                                        {'label': 'both gender', 'value': 'bothGender'},
                                        {'label': 'only males', 'value': 'male', 'disabled': False},
                                        {'label': 'only females', 'value': 'female', 'disabled': False}
                                    ],
                                    value=['bothGender', 'male', 'female']
                                )
                            ]
                        ),
                        #checkbox Trials
                        html.Div(id='div_trials',
                            style={'align': 'center'},
                            children=[
                                html.H4('Include patients from other trials:'),
                                dcc.Checklist(
                                    id='check_trials',
                                    value=[],
                                    labelStyle={'display': 'block'}
                                )
                            ]
                        ),
                        html.Div(id='div_displayoptions',
                            style={'align': 'left'},
                            children=[
                                html.Table(
                                    html.Tbody(
                                        [html.Tr(
                                            [html.Td("Include trials seperately (if false: include trials jointly)"),
                                            html.Td(
                                                daq.BooleanSwitch(
                                                    id='include_seperately',
                                                    on=True
                                                )
                                            )]
                                        ),
                                        html.Tr(
                                            [html.Td("Show interquartile ranges"),
                                            html.Td(
                                                daq.BooleanSwitch(
                                                    id='show_interquartile_ranges',
                                                    on=False
                                                )
                                            )]
                                        )]
                                    )
                                )
                            ]
                        )
                    ])

@app.callback(
    [Output(component_id='live-graph', component_property='figure'),
    Output(component_id='check_trials', component_property='options')],
    [Input(component_id='trial', component_property='value'),
    Input(component_id='user', component_property='value'),
    Input(component_id='dropdown', component_property='value'),
    Input(component_id='check_gender', component_property='value'),
    Input(component_id='check_trials', component_property='value'),
    Input(component_id='show_interquartile_ranges', component_property='on')])
def execute_query(trial_value, user_value, dropdown_value, gender_value, other_trials, show_interquartile_ranges):
    # get permission and build checklist for trials
    user = User.objects.get(id=user_value)
    trials = Trial.objects.all()
    trial_name = Trial.objects.get(id=trial_value).name
    check_trial_options = []
    for trial in trials:
        if has_object_permission('access_trial', user, trial) and trial.id != trial_value:
            check_trial_options.append({'label': trial.name, 'value': trial.id})

    check_trial_options = sorted(check_trial_options, key=itemgetter('label'))

    # get BCR-ABL/ABL values
    other_trials.append(trial_value)
    trials=other_trials
    diagnostic = Diagnostic.objects.filter(trial_id__in=trials, diagType_id = 1)

    diag_pivot = pivot(diagnostic, ['trial', 'targetId', 'sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
    df = pd.DataFrame(diag_pivot, columns = ['trial', 'targetId', 'sampleId', 'sampleDate', 'ABL', 'BCR-ABL/ABL'])
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

    df_sampleDateMin = df.groupby('targetId').agg({'sampleDate': 'min'}).reset_index()
    df_sampleDateMin = df_sampleDateMin.rename(columns={'sampleDate':'sampleDate_min'})
    df = df.merge(df_sampleDateMin, on = 'targetId')


    #get treatments
    treatment = TreatMedication.objects.filter(trial_id__in=trials)
    if treatment.exists():
        treat = treatment.values('targetId', 'dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit','medScheme')
        dfmedi = pd.DataFrame.from_records(data = treat)
        dfmedi_min = dfmedi.groupby('targetId').agg({'dateBegin':'min'}).reset_index()
        df = df.merge(dfmedi_min, on = 'targetId', how='left')
        '''
        if dropdown_value == 'graph1':
            df = df
        elif dropdown_value == 'graph2':
            df = df[df['drugName']=='Imatinib']
        elif dropdown_value == 'graph3':
            df = df[df['drugName']=='Dasatinib']
        '''
        # for R-Script "Median-calculation" again begin
        # TIME calculation if tretment exists
        df['TIME'] = (df['sampleDate']-df['dateBegin']) / np.timedelta64(1, 'M')
        # TIME calculation if treatment not exists
        df['TIME'].fillna((df['sampleDate']-df['sampleDate_min']) / np.timedelta64(1, 'M'), inplace=True)
    else:
        df['TIME'] = (df['sampleDate']-df['sampleDate_min']) / np.timedelta64(1, 'M')

    df = df.sort_values(by=['PatID','TIME'])

    # Exclude/Include gender by checkbox
    ####################################
    pat = PatientTrial.objects.filter(trial_id__in=trials)
    pat = pat.values('targetId', 'gender')
    dfpat = pd.DataFrame.from_records(data=pat)
    df = df.merge(dfpat, on='targetId')

    #  for R-Script "Median-calculation"
    ####################################
    
    # for each gender
    for gender in gender_value:
        if gender == 'bothGender':
            data_Rinput = df[['PatID', 'TIME', 'LRATIO', 'lQL','ND']].copy() 
        else:
            df_subset = df[df['gender']==gender]
            data_Rinput = df_subset[['PatID', 'TIME', 'LRATIO', 'lQL','ND']].copy() 
        # create tempfiles
        tf = tempfile.NamedTemporaryFile(suffix='.csv', dir='/usr/local/www/djangoprojects/predictDemo/media/documents/predictions/', delete=False)
        data_in = data_Rinput.to_csv(tf.name, sep=';', na_rep='Nan',index=False)
        args = [tf.name]
        command = 'Rscript'
        path2script = "/usr/local/www/djangoprojects/predictDemo/plotlydash/medianCalculations.R"
        #path2script = os.path.join(os.path.dirname(__file__), 'medianCalculations.R')
        cmd = [command, path2script] + args
        # R caclulation
        x = None
        try:
            x = subprocess.check_output(cmd, universal_newlines = True)
        except subprocess.CalledProcessError as e:
            x = e.output
        if x!='\n':
            if gender == 'bothGender':
                df_median = pd.read_csv(StringIO(x), sep=",")
            if gender == 'male':
                df_median_male = pd.read_csv(StringIO(x), sep=",")
            if gender == 'female':
                df_median_female = pd.read_csv(StringIO(x), sep=",")
        os.remove(tf.name)
        # end for R-Script calculation

    # graph
    graph_figure = go.Figure()

    ################################
    # add aggregation
    # median both genders
    try:
        if show_interquartile_ranges:
            # add 75.Quantil
            graph_figure.add_trace(go.Scatter(
                x=df_median['Time'],
                y=df_median['Quantile75'],
                line={'color':'grey', 'width': 2, 'dash':'dot'},
                showlegend=False,
                name='Quantile75 of both genders',
            ))
            # add 25. Quantil
            graph_figure.add_trace(go.Scatter(
                x=df_median['Time'],
            y=df_median['Quantile25'],
            name='interquartile range  of both genders',
            mode='lines',
            line={'color':'grey', 'width': 2, 'dash':'dot'},
            fill='tonexty',
            fillcolor='rgba(0,100,80,0.1)'
            ))
        # add median
        graph_figure.add_trace(go.Scatter(
            x=df_median['Time'],
            y=df_median['Median'],
            name='median of both gender',
            mode='lines', 
            line={'color':'black', 'width': 3}, 
        ))
    except:
        pass

    #lines for only females
    try:
        if show_interquartile_ranges:
            # add 75.Quantil female
            graph_figure.add_trace(go.Scatter(
                x=df_median_female['Time'],
                y=df_median_female['Quantile75'],
                line={'color':'coral', 'width': 2, 'dash':'dot'},
                showlegend=False,
                name='Quantile75 of females only',
            ))
            # add 25. Quantil female
            graph_figure.add_trace(go.Scatter(
                x=df_median_female['Time'],
            y=df_median_female['Quantile25'],
            name='interquartile range of females only',
            mode='lines',
            line={'color':'coral', 'width': 2, 'dash':'dot'},
            fill='tonexty',
            fillcolor='rgba(160,70,80,0.1)'
            ))
        # add median female
        graph_figure.add_trace(go.Scatter(
            x=df_median_female['Time'],
            y=df_median_female['Median'],
            name='median of females only',
            mode='lines', 
            line={'color':'coral', 'width': 3}, 
        ))
    except:
        pass

    # lines for only males
    try:
        if show_interquartile_ranges:
            # add 75.Quantil male
            graph_figure.add_trace(go.Scatter(
                x=df_median_male['Time'],
                y=df_median_male['Quantile75'],
                line={'color':'cornflowerblue', 'width': 2, 'dash':'dot'},
                showlegend=False,
                name='Quantile75 of males only',
            ))
            # add 25. Quantil male
            graph_figure.add_trace(go.Scatter(
                x=df_median_male['Time'],
            y=df_median_male['Quantile25'],
            name='interquartile range of males only',
            mode='lines',
            line={'color':'cornflowerblue', 'width': 2, 'dash':'dot'},
            fill='tonexty',
            fillcolor='rgba(16,16,90,0.1)'
            ))
        # add median male
        graph_figure.add_trace(go.Scatter(
            x=df_median_male['Time'],
            y=df_median_male['Median'],
            name='median of males only',
            mode='lines', 
            line={'color':'cornflowerblue', 'width': 3}, 
        ))
    except:
        pass

    ################################
    # add patient's time course
    if dropdown_value != 'graph1':
        patlist = sorted(df['targetId'].unique())
        patlist = patlist[::-1] # reverse order (ascending)
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
        title='BCR-ABL/ABL Aggregation from trial '+trial_name,
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
    return [graph_figure, check_trial_options]


if __name__ == '__main__':
    app.run_server(debug=True)