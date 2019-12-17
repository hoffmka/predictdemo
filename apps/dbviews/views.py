from django.db import connections
from django.shortcuts import render

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from ..trials.models import Trial
from .tables import sdv_DiagnosticValuesTable

# Create your views here.
def dbviews_list(request):
    '''
    List every db view
    '''
    return render(request, 'dbviews/dbviews_list.html', {
        
    })

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