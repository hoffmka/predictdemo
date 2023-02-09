from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import Group
from django.db.models import CharField, Value
from django.urls import reverse

from rolepermissions.mixins import HasRoleMixin

from . serializers import *

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import parsers

import json
import requests

from .. predictions.models import *

class PredictionView(HasRoleMixin, APIView):
    allowed_roles = 'dept_haematology'

    @staticmethod
    def _requestPSN(group, domain, localName, localIdentifier):
        ths_host = settings.MOSAIC_HOST
        url = ths_host + '/ths/rest/sessions'

        headers = {}
        headers['Connection'] = 'keep-alive'
        headers['Content-Type'] = 'application/json; charset=utf-8'
        headers['apiKey'] = settings.MOSAIC_APIKEY

        post_data = {
            "data": {
                "fields": {
                    "user_id": settings.MOSAIC_USERID,
                    "user_name": settings.MOSAIC_USER
                }
            }
        }

        r = requests.post(url, data=json.dumps(post_data), headers=headers)
        response = json.loads(r.text)
        sessionId = response['sessionId']

        # request TokenId
        url_token = ths_host+'/ths/rest/sessions/'+sessionId+'/tokens'
        # get ttp_targets
        group = Group.objects.get(name=group)
        post_data = {
            "type": "requestPSN",
            "method": "getOrCreate",
            "data": {
                "fields": {
                    "study_id": group.ttp_studyId,
                    "study_name": group.ttp_studyId,
                    "location_id": "loc1",
                    "location_name": "loc1",
                    "event": group.ttp_studyId+".requestPsn",
                    "reason": "new ic version",
                    "targetIdType": group.ttp_targetIdType,
            },
            }
        }
        r = requests.post(url_token, data=json.dumps(post_data), headers=headers)
        response = json.loads(r.text)
        tokenId = response['tokenId']

        url = ths_host+'/ths/rest/psn/request/'+tokenId
        post_data = {
            "patients": [
                {
                "index": "1",
                    "patientIdentifier": {
                    "domain": domain,
                    "name": localName,
                    "id": localIdentifier,
                    "type": "localIdentifier"
                    }
                }
            ]
        }

        r = requests.post(url, data=json.dumps(post_data, cls=DjangoJSONEncoder), headers=headers)
        response = json.loads(r.text)
        return response


    def post(self, request, format=None):

        if request.method == "POST":
            #post_data = json.loads(str(request.body))
            post_data=request.data
            group = post_data['group']
            domain = post_data['domain']
            localName = post_data['localName']
            localIdentifier = post_data['localIdentifier']


            # TTP request for targetId
            ttp_response = self._requestPSN(group, domain, localName,localIdentifier)
            
            if ("errors" in ttp_response):
                return Response("An error occurred during the request to the TTP server. Probably no patient was found.")
            else:
                prediction_targetId = ttp_response['patients'][0]['targetId']

                #Query predictions for targetId
                predictions = Prediction.objects.all().filter(targetId=prediction_targetId, status=1).annotate(url=Value("placeholder", output_field=CharField()))
                # get host
                host = request.META['HTTP_HOST']
                # get prefix
                if (request.META['SERVER_PORT']==443):
                    prefix = "https://"
                else:
                    prefix = "http://"
                for prediction in predictions:
                    prediction.url = prefix+host+reverse('predictions:prediction_detail', args=(prediction.id,))

                serializer=PredictionSerializer(predictions, many=True)
                #return Response(host)
                return Response({"predictions": serializer.data})

                