from django.urls import path

from . import views
from . views import *

app_name = 'predictions'

urlpatterns = [
    path('all/', PredictionListView.as_view(), name='prediction_all_list'),
    path('detail/<int:prediction_pk>/', PredictionDetailView.as_view(), name='prediction_detail'),
    path('list/', views.prediction_list, name='prediction_list'),
    path('create/recurrence_prob/', views.create_magpie_prediction_recurrence_prob, name='prediction_create_recurrence_prob'),
    path('create/modelfit/', views.create_magpie_prediction_modelfit, name='prediction_create_modelfit'),
    path('magpie_download/<int:prediction_id>/', views.magpie_download_jobresults, name='magpie_download_jobresults'),
]