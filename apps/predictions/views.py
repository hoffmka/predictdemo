from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Prediction

import json
import requests

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