from django.contrib import admin
from .models import Model, Prediction
# Register your models here.

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('targetId', 'model', 'magpieProjectId', 'magpieJobId', 'createdAt', 'createdBy')

admin.site.register(Model, ModelAdmin)
admin.site.register(Prediction, PredictionAdmin)