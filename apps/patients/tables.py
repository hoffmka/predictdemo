import django_tables2 as tables


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
    sampleId = tables.Column(verbose_name="Sample-ID")
    sampleDate = tables.DateColumn(verbose_name="Sample Date", format ='Y-m-d', order_by="sampleDate")
    ABL = tables.Column(verbose_name="ABL")
    BCR = tables.Column(verbose_name="BCR-ABL/ABL")
    #PID = tables.Column()

class CML_udv_treatmentTable(tables.Table):
    dateBegin = tables.DateColumn(format ='Y-m-d', verbose_name="Begin of Treatment")
    dateEnd = tables.DateColumn(format ='Y-m-d', verbose_name="End of Treatment")
    interval = tables.Column()
    intervalUnit = tables.Column(verbose_name = "Unit of Interval")
    drugName = tables.Column(verbose_name = "Drug")
    dosage = tables.Column()
    dosageUnit = tables.Column(verbose_name = "Unit of Dosage")
    medScheme = tables.Column(verbose_name = "Medication Scheme")
 
    def render_Dosage(self, value):
        return '{:.0f}'.format(value)
