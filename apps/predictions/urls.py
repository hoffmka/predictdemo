from django.urls import path

from . import views
from . views import *

app_name = 'predictions'

urlpatterns = [
    path('list', views.prediction_list, name='prediction_list'),
]