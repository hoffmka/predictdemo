from django.contrib import admin
from .models import Model, Project, Prediction

# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ('modelName', 'magpieModelId', 'active')
admin.site.register(Model, ModelAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('model', 'projectName', 'magpieProjectId')

admin.site.register(Project, ProjectAdmin)

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('project', 'targetId', 'magpieJobId', 'createdAt')

admin.site.register(Prediction, PredictionAdmin)