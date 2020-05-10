from django.contrib.auth.decorators import login_required
from django.db import connections
from django.db.models import F, Max

from django.shortcuts import redirect, render

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from django.views.generic import DetailView

from django_pivot.pivot import pivot

from ..trials.models import Trial
from .forms import THSSearchPsnByPatientForm #, ModelSelectionForm
from ..dbviews.models import Diagnostic, TreatMedication
from ..predictions.models import Prediction
from .tables import PatientsListTable, CML_udv_BcrAblRatioTable, CML_udv_treatmentTable

import json
import requests
# Create your views here.

@login_required
def patients_search(request):
    if request.method == 'POST':
        searchPsnByPatientForm = THSSearchPsnByPatientForm(request.POST)
        if searchPsnByPatientForm.is_valid():
            """
            HTTP request
            """
            from django.core.serializers.json import DjangoJSONEncoder
            from django.conf import settings
            # request SessionId

            ths_host = settings.MOSAIC_HOST
            url = ths_host + '/ths/rest/sessions'

            headers = {}
            headers['Connection'] = 'keep-alive'
            headers['Content-Type'] = 'application/json; charset=utf-8'
            headers['apiKey'] = 'admin'

            post_data = {
                "data": {
                    "fields": {
                        "user_id": "8989",
                        "user_name": "TestUser"
                    }
                }
            }

            r = requests.post(url, data=json.dumps(post_data), headers=headers)
            response = json.loads(r.text)
            uri_session = response['uri']

            # request TokenId
            url_token = uri_session+'/tokens'

            post_data = {
                "type": "requestPsnByPatient",
                "data": {
                    "fields": {
                        #"study_id": searchPsnByPatientForm.cleaned_data['domain'],
                        #"study_name": searchPsnByPatientForm.cleaned_data['domain'],
                        "study_id": "demo",
                        "study_name": "demo",
                        "location_id": "loc1",
                        "location_name": "loc1",
                        "event": "demo.requestPsn",
                        "reason": "new ic version",
                        "targetIdType": "mdat",
                        "options": {
                            "resultType": "simple"
                            }
                },
                }
            }

            r = requests.post(url_token, data=json.dumps(post_data), headers=headers)
            response = json.loads(r.text)
            tokenId = response['tokenId']

            # request pseudonym by patient (THS function name: F_RPP-T_OK-N_TC)
            url = ths_host + '/ths/rest/psn/requestPsnByPatient/'+ tokenId

            post_data = {
                "patients": [
                    {
                    "index": "1",
                    "patient": {
                        "firstName": searchPsnByPatientForm.cleaned_data['firstname'],
                        "lastName": searchPsnByPatientForm.cleaned_data['lastname'],
                        "gender": searchPsnByPatientForm.cleaned_data['gender'],
                        "birthplace": searchPsnByPatientForm.cleaned_data['birthplace'],
                        "birthdate": searchPsnByPatientForm.cleaned_data['birthdate']
                    }
                }
                ]
            }
            r = requests.post(url, data=json.dumps(post_data, cls=DjangoJSONEncoder), headers=headers)
            response = json.loads(r.text)
            try:
                targetId = response['patients'][0]['targetId']
            except:
                targetId = None
                errorCode = response['patients'][0]['errorCode']

            #domain = searchPsnByPatientForm.cleaned_data['domain']
            #domain = dict(searchPsnByPatientForm.fields['domain'].choices)[domain] # to get the label of the choice
            
            # Passing patient data to session
            request.session['patient_data'] = json.dumps(post_data['patients'][0]['patient'], cls=DjangoJSONEncoder)
            request.session['firstName'] = post_data['patients'][0]['patient']['firstName']
            request.session['targetId'] = targetId
            #request.session['domain'] = domain

            return redirect('patients:patient_mdat_view')
    else:
        searchPsnByPatientForm = THSSearchPsnByPatientForm()

    return render(request, 'patients/patients_search.html',{
        'searchPsnByPatientForm': searchPsnByPatientForm
        })

@login_required
def patient_mdat_view(request):
    # get patient data from session
    patient_data = json.loads(request.session['patient_data'])
    targetId = request.session['targetId']
    #domain = request.session['domain']

    # Are prediction available? If yes, then plot last prediction
    dash_context_model38 = None
    if Prediction.objects.filter(targetId = targetId, status = 1).exists():
        l = Prediction.objects.filter(targetId = targetId, status = 1).last()
        prediction_id = l.id
        dash_context_model38 = {"prediction_id": {"value": prediction_id}}

    #Otherwise plot bcr-abl/abl data, if bcr-abl/abl values available
    dash_context = None
    if Diagnostic.objects.filter(targetId = targetId, diagType_id = 1).exists():
        dash_context = {"targetId": {"value": targetId}}

    return render(request, 'patients/patient_mdat_view.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,
        'dash_context': dash_context,
        'dash_context_model38': dash_context_model38,
        })

@login_required
def patient_mdat_view_bcrabl(request):
    # get patient data from session
    patient_data = json.loads(request.session['patient_data'])
    targetId = request.session['targetId']
    #domain = request.session['domain']
    # get table with BCR-ABL / ABL ratio
    diagnostic = Diagnostic.objects.filter(targetId = targetId, diagType_id = 1) # diagType = PCR - BCR-ABL/ABL 
    diag_pivot = pivot(diagnostic, ['sampleId', 'sampleDate'], 'parameter_id__parameterName', 'value', aggregation=Max)
    # change key "BCR-ABL/ABL" to "BCR"
    if diag_pivot.exists():
        diag_pivot = diag_pivot.annotate(BCR=F('BCR-ABL/ABL')).values('sampleId', 'sampleDate', 'ABL', 'BCR')

    diagnosticTable = CML_udv_BcrAblRatioTable(data = diag_pivot, order_by="-sampleDate", empty_text = "No data available.")

    RequestConfig(request).configure(diagnosticTable) # Sort
    diagnosticTable.paginate(page=request.GET.get("page", 1), per_page=10) # Pagination
    export_format = request.GET.get('_export', None) # Export

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, diagnosticTable)
        return exporter.response("cml_udv_BcrAblRatio.{}".format(export_format))

    return render(request, 'patients/patient_mdat_view_bcrabl.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,
        'diagnosticTable': diagnosticTable
        })

@login_required
def patient_mdat_view_treatment(request):
    # get patient data from session
    patient_data = json.loads(request.session['patient_data'])
    targetId = request.session['targetId']
    #domain = request.session['domain']
    # get treatment data and pass to table
    treatment = TreatMedication.objects.filter(targetId = targetId)
    treatmentTable = CML_udv_treatmentTable(data = treatment, empty_text = "No data available.")

    RequestConfig(request).configure(treatmentTable) # Sort
    treatmentTable.paginate(page=request.GET.get("page", 1), per_page=10) # Pagination
    export_format = request.GET.get('_export', None) # Export

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, treatmentTable)
        return exporter.response("CML_udv_treatmentTable.{}".format(export_format))

    return render(request, 'patients/patient_mdat_view_treatment.html', {
        'patient_data' : patient_data,
        'targetId': targetId,
        #'domain': domain,
        'treatmentTable': treatmentTable
        })

def patients_list(request, trial_pk):
    trial = Trial.objects.get(id = trial_pk)
    hopt_studyid = trial.hopt_studyid
    with connections['HaematoOPT'].cursor() as cursor:
        cursor = cursor.execute("SELECT * from Patients_V WHERE StudyID = %s", [hopt_studyid])
        #results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns,row)))
    table = PatientsListTable(results)        

    table.paginate(page=request.GET.get("page", 1), per_page=25)

    return render(request, 'patients/patients_list.html', {
        "table": table
    })
