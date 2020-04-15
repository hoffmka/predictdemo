from django.urls import path

from . import views
from . views import *

app_name = 'patients'

urlpatterns = [
    path('list/<int:trial_pk>', views.patients_list, name='patients_list'),
    path('search', views.patients_search, name='patients_search'),
    path('patient', views.patient_mdat_view, name='patient_mdat_view'),
    path('patient/bcrabl', views.patient_mdat_view_bcrabl, name='patient_mdat_view_bcrabl'),
    path('patient/treatment', views.patient_mdat_view_treatment, name='patient_mdat_view_treatment'),
    path('patient/predict', views.patient_predict_view, name='patient_predict_view'),
    path('patient/predict/detail/<int:prediction_pk>/', views.prediction_detail, name='prediction_detail'),
    path('magpie', views.run_magpie_job, name='run_magpie_job'),
]