from django.contrib import admin
from .models import Dash, Model, Project, Prediction

# Register your models here.
class ModelAdmin(admin.ModelAdmin):
    list_display = ('modelName', 'magpieModelId', 'active', 'doi', 'description')
admin.site.register(Model, ModelAdmin)

class DashAdmin(admin.ModelAdmin):
    list_display = ('appname',)
admin.site.register(Dash, DashAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('model', 'projectName', 'magpieProjectId', 'dash', 'description')
admin.site.register(Project, ProjectAdmin)

class PredictionAdmin(admin.ModelAdmin):
    list_display = ('project', 'targetId', 'magpieJobId', 'createdAt', 'status')
admin.site.register(Prediction, PredictionAdmin)

