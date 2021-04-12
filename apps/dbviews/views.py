from django.db import connections
from django.shortcuts import render

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from django.views.generic import DetailView

from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin

from predictDemo.roles.mixins import HasObjectPermissionMixin

from ..trials.models import Trial
from . models import Diagnostic, TreatMedication
from .tables import sdv_DiagnosticValuesTable, TrialDiagnosticTable, TrialMedicationTable

import json
import requests

# Create your views here.
def dbviews_list(request):
    '''
    List every db view
    '''
    return render(request, 'dbviews/dbviews_list.html', {
        
    })

# For Research - Query HOPT Database
def sdv_diagnostic_values(request, trial_pk):
    trial = Trial.objects.get(id = trial_pk)
    hopt_studyid = trial.hopt_studyid
    with connections['HaematoOPT'].cursor() as cursor:
        cursor = cursor.execute("SELECT * from CheckupValues_V WHERE StudyID = %s", [hopt_studyid])
        #results = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns,row)))
    sdv_diagnostic_values_table = sdv_DiagnosticValuesTable(results)        

    sdv_diagnostic_values_table.paginate(page=request.GET.get("page", 1), per_page=25)

    return render(request, 'dbviews/sdv_diagnostic_values.html', {
        "sdv_diagnostic_values_table": sdv_diagnostic_values_table
    })

class TrialDiagnosticDetailView(HasObjectPermissionMixin, ExportMixin, SingleTableMixin, DetailView):
    """
    This view lists all diagnostic values from a trial
    """
    checker_name = 'access_trial'
    model = Trial
    pk_url_kwarg = 'trial_pk'
    table_class = TrialDiagnosticTable
    context_table_name = 'diagnosticTable'
    table_pagination = {"per_page": 10}
    template_name = 'dbviews/diagnostic_trial.html'
    export_formats = ("csv", "xls")

    def get_table_data(self, **kwargs):
        """
        #Filtering diagnostic values by trial_pk
        """
        trial = Trial.objects.get(id=self.kwargs['trial_pk'])
        if (trial.group is not None):
            qs = Diagnostic.objects.filter(targetId__startswith = trial.group.ttp_targetIdType)
        else:
            qs = []
        return qs

    # def get_queryset(self, **kwargs):
    #     """
    #     Filtering diagnostics by project_pk
    #     """
    #     qs = ProtocolModel.objects.filter(project = self.kwargs['project_pk']).order_by('-date')
    #     return qs

    def get_context_data(self, **kwargs):
        """
        Passing trial details to template
        """
        context = super(TrialDiagnosticDetailView, self).get_context_data(**kwargs)
        context['trial_pk']= self.kwargs['trial_pk']
        context['trial'] = Trial.objects.get(id = self.kwargs['trial_pk'])
        return context

class TrialMedicationDetailView(HasObjectPermissionMixin, ExportMixin, SingleTableMixin, DetailView):
    """
    This view lists all medications from a trial
    """
    checker_name = 'access_trial'
    model = Trial
    pk_url_kwarg = 'trial_pk'
    table_class = TrialMedicationTable
    context_table_name = 'medicationTable'
    table_pagination = {"per_page": 10}
    template_name = 'dbviews/medication_trial.html'
    export_formats = ("csv", "xls")

    def get_table_data(self, **kwargs):
        """
        #Filtering medication values by trial_pk
        """
        trial = Trial.objects.get(id=self.kwargs['trial_pk'])
        if (trial.group is not None):
            qs = TreatMedication.objects.filter(targetId__startswith = trial.group.ttp_targetIdType)
        else:
            qs = []
        return qs