from django.urls import path

from . import views
from . views import *

app_name = 'shiny'

urlpatterns = [
    path('shinyExample/', views.shiny, name='shiny'),
    path('shinyExample_contents/', views.shiny_contents, name='shiny_contents'),
]