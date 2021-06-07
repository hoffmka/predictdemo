from django.contrib import admin
from .models import DiagType, DiagParameter, Diagnostic, TreatMedication

# Register your models here.
class TreatMedicationAdmin(admin.ModelAdmin):
    list_display = ('trial', 'targetId', 'dateBegin', 'dateEnd', 'interval', 'intervalUnit', 'drugName', 'dosage', 'dosageUnit', 'medScheme', 'createdAt', 'updatedAt')

admin.site.register(TreatMedication, TreatMedicationAdmin)

class DiagTypeAdmin(admin.ModelAdmin):
    list_display = ('diagTypeName',)

admin.site.register(DiagType, DiagTypeAdmin)

class DiagParameterAdmin(admin.ModelAdmin):
    list_display = ('parameterName',)

admin.site.register(DiagParameter, DiagParameterAdmin)

class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('diagType', 'trial', 'targetId', 'sampleId', 'sampleDate', 'parameter', 'value', 'unit', 'createdAt', 'updatedAt')

admin.site.register(Diagnostic, DiagnosticAdmin)

