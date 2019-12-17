from django.contrib import admin
from .models import DashSimpleModel

# Register your models here.

class DashSimpleModelAdmin(admin.ModelAdmin):
    list_display = ('x', 'y')

admin.site.register(DashSimpleModel, DashSimpleModelAdmin)