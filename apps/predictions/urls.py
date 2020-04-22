from django.urls import path

from . import views
from . views import *

app_name = 'predictions'

urlpatterns = [
    path('list', views.prediction_list, name='prediction_list'),
    path('magpie_download_jobresults', views.magpie_download_jobresults, name='magpie_download_jobresults'),
    path('Rtest', views.test_R, name='test_R'), # only for testing R integration
]