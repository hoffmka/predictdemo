from django.urls import path

from . import views
from . views import *

app_name = 'udv_destiny'

urlpatterns = [
    path('view1/', views.cml_destiny_view1, name='cml_destiny_view1'),
]