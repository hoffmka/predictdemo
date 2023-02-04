from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Max, Q
#from django.http import HttpResponse
from django.shortcuts import redirect, render

from django_pivot.pivot import pivot

from djqscsv import write_csv

from .models import Prediction, Project
from .tables import *

from ..dbviews.models import Diagnostic, TreatMedication

from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin

import json
import os
import requests
import subprocess

class PredictionListView(SingleTableMixin, ListView):
    """
    This view lists predictions
    """
    queryset = Prediction.objects.all().order_by('-id')
    context_table_name = 'predictionListTable'
    table_class = PredictionListTable
    table_pagination = {"per_page": 10}
    template_name = 'predictions/prediction_all_list.html'

class PredictionDetailView(DetailView):
    """
    This view displays detail information of a prediction
    """
    model = Prediction
    template_name = 'predictions/prediction_detail.html'
    pk_url_kwarg = 'prediction_pk'

    def get_context_data(self, *args, **kwargs):
        # passing prediction_id as initial value to context
        context = super().get_context_data(*args, **kwargs)
        prediction_id = self.kwargs['prediction_pk']
        # dash app name
        prediction = Prediction.objects.get(id = prediction_id)
        context['dash_app'] = prediction.project.dash.appname
        # initial value
        dash_context = {"prediction_id": {"value": prediction_id}}
        context['dash_context'] = dash_context
        return context

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
        dash_context_simple = {"prediction_id": {"value": prediction_id}, "dropdown": {"value": "simple"}}
        dash_context_expert = {"prediction_id": {"value": prediction_id}, "dropdown": {"value": "expert"}}
        dash_context_dict[prediction_id] = {}
        dash_context_dict[prediction_id]['simple'] = dash_context_simple
        dash_context_dict[prediction_id]['expert'] = dash_context_expert

    return render(request, 'predictions/prediction_list.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,
        'predictions': predictions,
        'dash_context_dict': dash_context_dict,
        })

@login_required
def create_magpie_prediction_recurrence_prob(request):
    # new prediction object
    targetId = request.session['targetId']
    projectId = 6

    n = Prediction.objects.create(project_id = projectId, targetId = targetId)
    prediction_id = n.id

    # save patdata
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', str(prediction_id)))):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', str(prediction_id))))

    treatMedication = TreatMedication.objects.filter(targetId = targetId)
    with open(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_medi.csv'))), 'wb') as csv_file:
        write_csv(treatMedication, csv_file, delimiter=';')
    
    diagnostic = Diagnostic.objects.filter(targetId = targetId, diagType_id = 1) # diagType = PCR - BCR-ABL/ABL

    #exclude observations after stop
    if treatMedication.filter(medScheme='stop').exists():
        diagnostic = diagnostic.filter(sampleDate__lte = treatMedication.filter(medScheme='stop')[0].dateBegin)

    diag_pivot = pivot(diagnostic, ['sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
    with open(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_pcr.csv'))), 'wb') as csv_file:
        write_csv(diag_pivot, csv_file, delimiter=';')

    # create magpie job
    magpie_url = settings.MAGPIE_URL
    magpie_user = settings.MAGPIE_USER
    magpie_password = settings.MAGPIE_PASSWORD

    # magpie ids for project and model
    project = Project.objects.get(id = projectId)
    magpie_project_id = str(project.magpieProjectId)
    magpie_model_id = str(project.model.magpieModelId)

    df_pcr = os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_pcr.csv')))
    df_treat = os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_medi.csv')))

    args = [magpie_user, magpie_password, magpie_url, magpie_project_id, magpie_model_id, df_pcr, df_treat]

    command = 'Rscript'
    path2script = os.path.join(os.path.dirname(__file__), 'Rscripts/magpie_create_job.R')
    cmd = [command, path2script] + args

    x = None
    try:
        x = subprocess.check_output(cmd, universal_newlines = True)
    except subprocess.CalledProcessError as e:
        x = e.output

    # update prediction with magpie_job_id
    stdout_dict = {}
    i = 0
    for line in x.split('\n'):
        print("%r" % line)
        i = i + 1
        stdout_dict[i] = line
    magpie_job_id = stdout_dict[3]

    Prediction.objects.filter(id = prediction_id).update(magpieJobId = magpie_job_id)

    return redirect('predictions:prediction_list')

@login_required
def create_magpie_prediction_modelfit(request):
    # new prediction object
    targetId = request.session['targetId']
    projectId = 5

    n = Prediction.objects.create(project_id = projectId, targetId = targetId)
    prediction_id = n.id

    # save patdata
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', str(prediction_id)))):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', str(prediction_id))))

    treatMedication = TreatMedication.objects.filter(targetId = targetId)
    with open(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_medi.csv'))), 'wb') as csv_file:
        write_csv(treatMedication, csv_file, delimiter=';')

    diagnostic = Diagnostic.objects.filter(targetId = targetId, diagType_id = 1) # diagType = PCR - BCR-ABL/ABL 
    diag_pivot = pivot(diagnostic, ['sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
    with open(os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_pcr.csv'))), 'wb') as csv_file:
        write_csv(diag_pivot, csv_file, delimiter=';')

    # create magpie job
    magpie_url = settings.MAGPIE_URL
    magpie_user = settings.MAGPIE_USER
    magpie_password = settings.MAGPIE_PASSWORD

    # magpie ids for project and model
    project = Project.objects.get(id = projectId)
    magpie_project_id = str(project.magpieProjectId)
    magpie_model_id = str(project.model.magpieModelId)

    df_pcr = os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_pcr.csv')))
    df_treat = os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', os.path.join(str(prediction_id), 'patdata_medi.csv')))

    args = [magpie_user, magpie_password, magpie_url, magpie_project_id, magpie_model_id, df_pcr, df_treat]

    command = 'Rscript'
    path2script = os.path.join(os.path.dirname(__file__), 'Rscripts/magpie_create_job.R')
    cmd = [command, path2script] + args

    x = None
    try:
        x = subprocess.check_output(cmd, universal_newlines = True)
    except subprocess.CalledProcessError as e:
        x = e.output

    # update prediction with magpie_job_id
    stdout_dict = {}
    i = 0
    for line in x.split('\n'):
        print("%r" % line)
        i = i + 1
        stdout_dict[i] = line
    magpie_job_id = stdout_dict[3]

    Prediction.objects.filter(id = prediction_id).update(magpieJobId = magpie_job_id)

    return redirect('predictions:prediction_list')

@login_required
def magpie_download_jobresults(request, prediction_id):
    # get prediction by id
    prediction = Prediction.objects.get(id = prediction_id)

    # variable number of args in a list
    magpie_url = settings.MAGPIE_URL
    magpie_user = settings.MAGPIE_USER
    magpie_password = settings.MAGPIE_PASSWORD
    magpie_project_id = str(prediction.project.magpieProjectId)
    magpie_model_id = str(prediction.project.model.magpieModelId)
    magpie_job_id = str(prediction.magpieJobId)
    media_dir = os.path.join(settings.MEDIA_ROOT, os.path.join('documents/predictions', str(prediction_id)))

    # run R script for job download
    command = 'Rscript'
    #path2script = '/usr/local/www/djangoprojects/predictDemo/apps/predictions/Rscripts/magpie_download_jobresults.R'
    path2script = os.path.join(os.path.dirname(__file__), 'Rscripts/magpie_download_jobresults.R')
    args = [magpie_user, magpie_password, magpie_url, magpie_project_id, magpie_model_id, magpie_job_id, media_dir]

    cmd = [command, path2script] + args

    x = None
    try:
        x = subprocess.check_output(cmd, universal_newlines = True)
    except subprocess.CalledProcessError as e:
        x = e.output

    # update prediction with magpie_job_id
    stdout_dict = {}
    i = 0
    for line in x.split('\n'):
        print("%r" % line)
        i = i + 1
        stdout_dict[i] = line
    
    # set prediction status (to finished)
    job_status = None
    try:
        job_status = stdout_dict[4]
    except:
        pass
    if job_status == '2':
        Prediction.objects.filter(id = prediction_id).update(status = 1)

    #failed
    if Prediction.objects.filter(id = prediction_id, status = 1).exists:
        try:
            job_status = stdout_dict[3]
        except:
            pass
        if job_status == '1':
            Prediction.objects.filter(id = prediction_id).update(status = 2)

    return redirect('predictions:prediction_all_list')