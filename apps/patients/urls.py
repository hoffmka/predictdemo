from django.urls import path

from . import views
from . views import *

app_name = 'patients'

urlpatterns = [
    path('list/<int:trial_pk>', views.patients_list, name='patients_list'),
    path('search', views.patients_search, name='patients_search'),
    path('patient', views.patient_mdat_view, name='patient_mdat_view'),
    path('patient/shiny', views.shiny, name='shiny'),
    path('shiny_contents/', views.shiny_contents, name='shiny_contents'),
]