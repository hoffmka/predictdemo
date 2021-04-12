import django_tables2 as tables
from . models import Diagnostic, TreatMedication

class sdv_DiagnosticValuesTable(tables.Table):
    CheckupID = tables.Column(visible=False)
    PatientID = tables.Column(visible=False)
    StudyID = tables.Column(visible=False)
    StudyCode = tables.Column(verbose_name="Study")
    PatientNumber = tables.Column(verbose_name="Patient Number")
    OrderNumber = tables.Column(verbose_name="Order Number")
    DateOfCheckup = tables.DateColumn(verbose_name="Diagn. Date")
    CheckupTypeID = tables.Column(visible=False)
    CheckupType = tables.Column(verbose_name="Diagnostic Type")
    Material = tables.Column(visible=False)
    CheckupStatus = tables.Column(visible=False)
    Comment = tables.Column(verbose_name="Comment to diagnostic")
    CheckupCreatedAt = tables.DateColumn(visible=False)

class TrialDiagnosticTable(tables.Table):
    targetId = tables.Column(verbose_name="Patient pseudonym")

    class Meta:
        model = Diagnostic
        fields = ("diagType", "targetId", "sampleId", "sampleDate", "parameter", "value", "unit", "createdAt", "updatedAt")
        empty_text= 'There are no diagnostics available.'

class TrialMedicationTable(tables.Table):
    targetId = tables.Column(verbose_name="Patient pseudonym")
    createdAt = tables.Column(visible=False)
    updatedAt = tables.Column(visible=False)

    class Meta:
        model = TreatMedication
        fields = ("targetId", "dateBegin", "dateEnd", "interval", "intervalUnit", "drugName", "dosage", "dosageUnit", "medScheme", "createdAt", "updatedAt")
        empty_text= 'There are no medications available.'
