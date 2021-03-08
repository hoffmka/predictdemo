from django.urls import path

from . import views
from . views import *

app_name = 'predictions'

urlpatterns = [
    path('all/', PredictionListView.as_view(), name='prediction_all_list'),
    path('detail/<int:prediction_pk>/', PredictionDetailView.as_view(), name='prediction_detail'),
    path('list/', views.prediction_list, name='prediction_list'),
    path('create/', views.create_magpie_prediction, name='prediction_create'),
    path('magpie_download/<int:prediction_id>/', views.magpie_download_jobresults, name='magpie_download_jobresults'),
]