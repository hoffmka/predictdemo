import django_tables2 as tables

class udvDestinyView1Table(tables.Table):
    StudyPatientNumber = tables.Column()
    DateOfCheckup = tables.DateColumn(format ='Y-m-d')
    BCRABL_ABL_Ratio_i_PB = tables.Column()
    BCRABL_copies_i_PB = tables.Column()
    ABL_Control_9_99_E99 = tables.Column()
    
