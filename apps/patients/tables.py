import django_tables2 as tables
from django_tables2.utils import A 
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Prediction

class PatientsListTable(tables.Table):
    PatientID = tables.Column()
    PatientStudyID = tables.Column()
    StudyID = tables.Column()
    StudyPatientNumber = tables.Column()
    Gender = tables.Column()
    EntryDate = tables.Column() #tables.DateColumn(format ='Y-m-d')
    StudyCode = tables.Column()

class CML_udv_BcrAblRatioTable(tables.Table):
    #PatientID = tables.Column()
    SampleID = tables.Column()
    SampleDate = tables.DateColumn(format ='Y-m-d')
    ControlGene = tables.Column(verbose_name="Control Gene")
    BCRABLRatio = tables.Column()
    #PID = tables.Column()

    def render_ControlGene(self, value):
        return '{:.0f}'.format(value)

class CML_udv_treatmentTable(tables.Table):
    TreatmentValueDateBegin = tables.DateColumn(format ='Y-m-d', verbose_name="Begin of Treatment")
    TreatmentValueDateEnd = tables.DateColumn(format ='Y-m-d', verbose_name="End of Treatment")
    Interval = tables.Column()
    IntervalUnit = tables.Column(verbose_name="Unit of Interval")
    Name = tables.Column()
    Dosage = tables.Column()
    DosageUnit = tables.Column(verbose_name="Unit of Dosage")
 
    def render_Dosage(self, value):
        return '{:.0f}'.format(value)


class PredictionTable(tables.Table):
    detail = tables.LinkColumn('patients:prediction_detail', args=[A('pk')], orderable=False, empty_values=())
    targetId = tables.Column()
    model = tables.Column()
    magpieProjectId = tables.Column()
    magpieJobId = tables.Column()
    createdAt = tables.DateColumn(format ='Y-m-d', verbose_name="Created at")
    createdBy = tables.Column()

    def render_detail(self, record):
        return mark_safe('<a class="viewdetailslink" href='+reverse("patients:prediction_detail", args=[record.pk])+'></a>')