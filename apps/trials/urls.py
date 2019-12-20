from django.urls import path

from . import views
from . views import *

app_name = 'trials'

urlpatterns = [
    path('list/', TrialListView.as_view(), name='trials_list'),
    path('add/', TrialCreateView.as_view(), name='trials_create'),
    path('delete/<int:trial_pk>/', TrialDeleteView.as_view(), name='trials_delete'),
    path('detail/<int:trial_pk>/', TrialDetailView.as_view(), name='trials_detail'),
    path('edit/<int:trial_pk>/', TrialUpdateView.as_view(), name='trials_update'),
    path('uploads/<int:trial_pk>/', TrialUploadListView.as_view(), name='trials_file_list'),    
    path('upload/<int:trial_pk>/', views.trials_file_upload, name='trials_file_upload'),
    path('upload/detail/<int:document_pk>/', TrialUploadDetailView.as_view(), name='trials_upload_detail'),
    path('upload/edit/<int:document_pk>/', TrialUploadUpdateView.as_view(), name='trials_upload_update'),
    path('upload/delete/<int:document_pk>/', TrialUploadDeleteView.as_view(), name='trials_upload_delete'),
]