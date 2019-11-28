from django.db import connections
from django.shortcuts import render

# Create your views here.
def cml_destiny_view1(request):
    with connections['HaematoOPT'].cursor() as cursor:
        cursor = cursor.execute('Select * from studies')
        columns = [column[0] for column in cursor.description]
        studies = []
        for row in cursor.fetchall():
            studies.append(dict(zip(columns,row)))
    
    return render(request, 'udv_destiny/cml_destiny_view1.html', {
        "studies": studies,
    })