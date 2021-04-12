from django.urls import path

from . import views
from . views import *

app_name = 'dbviews'

urlpatterns = [
    #path('diagnostic_values/<int:trial_pk>/', views.sdv_diagnostic_values, name='sdv_diagnostic_values'),
    path('diagnostic_values/<int:trial_pk>/', TrialDiagnosticDetailView.as_view(), name='trial_diagnostic_values'),
    path('medication/<int:trial_pk>/', TrialMedicationDetailView.as_view(), name='trial_medication_values'),
]