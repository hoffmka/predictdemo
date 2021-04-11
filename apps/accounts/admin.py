from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group

class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'ttp_studyId', 'ttp_targetIdType')

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)