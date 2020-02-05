from django.urls import path

from . import views
from . views import *

app_name = 'patients'

urlpatterns = [
    path('search', views.patients_search, name='patients_search'),
    path('patient', views.patient_mdat_view, name='patient_mdat_view'),
    path('list/<int:trial_pk>', views.patients_list, name='patients_list'),
]