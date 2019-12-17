import django_tables2 as tables

class PatientsListTable(tables.Table):
    PatientID = tables.Column()
    PatientStudyID = tables.Column()
    StudyID = tables.Column()
    StudyPatientNumber = tables.Column()
    Gender = tables.Column()
    EntryDate = tables.Column() #tables.DateColumn(format ='Y-m-d')
    StudyCode = tables.Column()