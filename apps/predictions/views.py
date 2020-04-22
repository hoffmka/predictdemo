from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.shortcuts import render

from .models import Prediction

import json
import os
import requests
import subprocess

@login_required
def prediction_list(request):
    # get patient data from session
    patient_data = json.loads(request.session['patient_data'])
    targetId = request.session['targetId']
    #domain = request.session['domain']
    predictions = Prediction.objects.filter(targetId = targetId).order_by('-id')
    #initial_arguments for dash app
    dash_context_dict = {}
    for prediction in predictions:
        prediction_id = prediction.pk
        dash_context = {"prediction_id": {"value": prediction_id}}
        dash_context_dict[prediction_id] = dash_context

    return render(request, 'predictions/prediction_list.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,
        'predictions': predictions,
        'dash_context_dict': dash_context_dict,
        })

@login_required
def magpie_download_jobresults(request):
    command = 'Rscript'
    path2script = os.path.join(os.path.dirname(__file__), 'Rscripts/magpie_download_jobresults.R')

    # variable number of args in a list
    magpie_user = 'katja.hoffmann@tu-dresden.de'
    magpie_password = 'kh09:L'
    magpie_url = 'http://10.25.69.145'
    magpie_project_id = '95'
    magpie_model_id = '38'
    magpie_job_id = '426'
    media_dir = '/usr/local/www/djangoprojects/predictDemo/media/documents/predictions/1'

    args = [magpie_user, magpie_password, magpie_url, magpie_project_id, magpie_model_id, magpie_job_id, media_dir]

    cmd = [command, path2script] + args

    x = None
    try:
        x = subprocess.check_output(cmd, universal_newlines = True)
    except subprocess.CalledProcessError as e:
        x = e.output
    
    # go through stdout, build dict and retrieve output value
    stdout_dict = {}
    i = 0
    for line in x.split('\n'):
        print("%r" % line)
        i = i + 1
        stdout_dict[i] = line
    str7 = stdout_dict[7] = stdout_dict[7]
    str7 = str7[5:-1]

    return render(request, 'predictions/Rtest.html', {
        'x': x,
        'stdout_dict': stdout_dict
    })


@login_required
def test_R(request):
    #Define command and arguments
    command = 'Rscript'
    path2script = os.path.join(os.path.dirname(__file__), 'Rscripts/myscript.R')

    # variable number of args in a list
    args =['11', '3', '9', '42']

    # build subprocess command
    cmd = [command, path2script] + args

    # check_output will run the command and store to results
    x = None
    try:
        x = subprocess.check_output(cmd, universal_newlines = True)
    except subprocess.CalledProcessError as e:
        x = e.output

    #print('The maximum of the nubers is:', x)

    return render(request, 'predictions/Rtest.html', {
        'x': x
    })