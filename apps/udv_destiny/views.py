from django.db import connections
from django.shortcuts import render

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

from .tables import udvDestinyView1Table

# Create your views here.
def cml_destiny_view1(request):
    with connections['HaematoOPT'].cursor() as cursor:
        cursor = cursor.execute('select * from udv_DESTINY_BCRABL_calculated_V')
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns,row)))
    table = udvDestinyView1Table(results)

    table.paginate(page=request.GET.get("page", 1), per_page=10)

    #RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("udvDestinyView1.{}".format(export_format))

    return render(request, 'udv_destiny/cml_destiny_view1.html', {
        "table": table,
    })