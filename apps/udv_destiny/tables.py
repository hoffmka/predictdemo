
import django_tables2 as tables

class udvDestinyView1Table(tables.Table):
    StudyPatientNumber = tables.Column()
    DateOfCheckup = tables.DateColumn(format ='Y-m-d')

#table = udvDestinyView1Table(data)