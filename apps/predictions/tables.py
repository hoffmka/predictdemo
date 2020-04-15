import django_tables2 as tables
from django_tables2.utils import A 
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Prediction

class PredictionTable(tables.Table):
    detail = tables.LinkColumn('predictions:prediction_detail', args=[A('pk')], orderable=False, empty_values=())
    targetId = tables.Column()
    project = tables.Column()
    magpieJobId = tables.Column()
    createdAt = tables.DateColumn(format ='Y-m-d', verbose_name="Created at")
    createdBy = tables.Column()

    def render_detail(self, record):
        return mark_safe('<a class="viewdetailslink" href='+reverse("predictions:prediction_detail", args=[record.pk])+'></a>')