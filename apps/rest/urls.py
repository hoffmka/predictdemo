from django.urls import path, include
from rest_framework import routers

from . import views
from . views import *

app_name = 'rest'

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('request/predictions/', PredictionView.as_view())
]