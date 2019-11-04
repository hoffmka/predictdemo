from django.contrib.auth.models import User
from django.db import models
import os
# Create your models here.

class Trial(models.Model):
    studyCode = models.CharField(max_length = 20, unique=True)
    name = models.CharField(max_length = 40)
    description = models.TextField(blank = True)
    clinicalTrials = models.CharField(max_length = 40, blank = True)
    eudraCT = models.CharField(max_length = 40, blank = True)
    createdAt = models.DateTimeField(auto_now_add = True)
    createdBy = models.ForeignKey(User, on_delete = models.CASCADE, default = None)  


    def __str__(self):
        return '%s' % (self.name)

class TrialPermission(models.Model):
    PERMISSION = (
        (0, 'view'),
        (1, 'change (and view)'),
        (2, 'delete, (and view + change'),
        (3, 'admin, (and view + change + delete)')
    )
    trial = models.ForeignKey(Trial, on_delete = models.CASCADE, default = None)
    user = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    permission = models.IntegerField(choices = PERMISSION, default = 0)
    createdAt = models.DateTimeField(auto_now_add = True)
    createdBy = models.ForeignKey(User, related_name='trial_createdBy', on_delete = models.CASCADE, default = None)

class Document(models.Model):
    document = models.FileField(upload_to = 'documents/trials/%Y/%m/%d')
    description = models.TextField(max_length = 255, blank = True)
    trial = models.ForeignKey(Trial, on_delete = models.CASCADE, default = None)
    uploaded_at = models.DateTimeField(auto_now_add = True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default = None)

    def filename(self):
        return os.path.basename(self.document.name)