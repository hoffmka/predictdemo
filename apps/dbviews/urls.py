from django.urls import path

from . import views
from . views import *

app_name = 'dbviews'

urlpatterns = [
    path('list/', views.dbviews_list, name='dbviews_list'),
    path('diagnostic_values/<int:trial_pk>/', views.sdv_diagnostic_values, name='sdv_diagnostic_values'),
]