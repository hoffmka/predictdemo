from django.contrib.auth.decorators import login_required
from django.db import connections

from django.shortcuts import redirect, render

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from ..trials.models import Trial
from .forms import THSSearchPsnByPatientForm #, ModelSelectionForm
from .tables import PatientsListTable

# Create your views here.

@login_required
def patients_search(request):
    if request.method == 'POST':
        searchPsnByPatientForm = THSSearchPsnByPatientForm(request.POST)
        if searchPsnByPatientForm.is_valid():
            """
            TTP request
            """
            import json
            import requests
            from django.core.serializers.json import DjangoJSONEncoder
            from django.conf import settings
            # request SessionId

            ths_host = settings.MOSAIC_HOST
            url = ths_host + '/test/rest/sessions'

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
                "callback": "http://localhost:8080/test/rest/test/callback/receive"
                }
            }

            r = requests.post(url_token, data=json.dumps(post_data), headers=headers)
            response = json.loads(r.text)
            tokenId = response['tokenId']

            # request pseudonym by patient (THS function name: F_RPP-T_OK-N_TC)
            url = ths_host + '/test/rest/psn/requestPsnByPatient/'+ tokenId

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
            tempId = response['patients'][0]['tempId']

            domain = searchPsnByPatientForm.cleaned_data['domain']
            domain = dict(searchPsnByPatientForm.fields['domain'].choices)[domain] # to get the label of the choice
            
            #modelSelectionForm = ModelSelectionForm()

            # render PatientRequestList
            return render(request, 'patients/patient_mdat_view.html', {
                'patient_data': post_data['patients'][0]['patient'],
                #'uri_session': uri_session,
                #'tokenId': tokenId,
                #'response': response,
                'domain': domain,
                'tempId': tempId,
                #'modelSelectionForm': modelSelectionForm,
            })
    else:
        searchPsnByPatientForm = THSSearchPsnByPatientForm()

    return render(request, 'patients/patients_search.html',{
        'searchPsnByPatientForm': searchPsnByPatientForm
        })

#def patient_mdat_view(request):
#    return render(request, 'patients/patient_mdat_view.html', {})

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

