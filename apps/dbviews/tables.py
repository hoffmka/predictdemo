import django_tables2 as tables

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