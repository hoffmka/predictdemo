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
