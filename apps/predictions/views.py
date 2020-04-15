from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django_tables2.config import RequestConfig
from .models import Prediction
from .tables import PredictionTable

import json
import requests

@login_required
def prediction_list(request):
    # get patient data from session
    patient_data = json.loads(request.session['patient_data'])
    targetId = request.session['targetId']
    #domain = request.session['domain']
    predictionTable = PredictionTable(Prediction.objects.all())

    return render(request, 'predictions/prediction_list.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,
        'predictionTable': predictionTable
        })

def prediction_detail(request, prediction_pk):
    """
    This view will retrieve the details for a prediction
    """
    patient_data = json.loads(request.session['patient_data'])
    targetId = request.session['targetId']
    prediction = Prediction.objects.get(id = prediction_pk) 

    return render(request, 'predictions/prediction_detail.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,      
        'prediction': prediction 
    })