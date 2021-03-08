import django_tables2 as tables
from django_tables2.utils import A 
from django.urls import reverse
from django.utils.safestring import mark_safe

from . models import Prediction

class PredictionListTable(tables.Table):
    id = tables.LinkColumn('predictions:prediction_detail', args=[A('pk')])
    class Meta:
        model = Prediction
        fields = ("id", "project", "targetId", "magpieJobId", "status", "createdAt")
        empty_text= 'There are no persons available.'