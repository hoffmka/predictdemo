from django.urls import include, path

from . import views

app_name = 'd3plots'

urlpatterns = [
    path('test/', views.demo_piechart, name='demo_piechart'),
]