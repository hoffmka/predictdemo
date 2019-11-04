from django.contrib import admin
from .models import Trial, TrialPermission, Document
# Register your models here.

class TrialAdmin(admin.ModelAdmin):
    list_display = ('studyCode', 'name', 'description', 'clinicalTrials', 'eudraCT', 'createdAt', 'createdBy')

class TrialPermissionAdmin(admin.ModelAdmin):
    list_display = ('trial', 'user', 'permission', 'createdAt', 'createdBy')

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('description', 'document', 'trial','uploaded_at', 'uploaded_by')

admin.site.register(Document, DocumentAdmin)
admin.site.register(Trial, TrialAdmin)
admin.site.register(TrialPermission, TrialPermissionAdmin)