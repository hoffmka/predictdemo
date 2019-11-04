from django.db import models
# from .. trials.models import *

# Create your models here.
# class PatientModel(models.Model):
#     pid = models.CharField(max_length=40, blank = True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     #createdBy ?


# class PatientStudyModel(models.Model):
#     patient = models.ForeignKey(PatientModel, on_delete = models.CASCADE)
#     trial = models.ForeignKey(Trial, on_delete = models.CASCADE)
#     studyPatientNumber = models.CharField(max_length = 40)
#     excluded = models.BooleanField(default = False)
#     excludedAt = models.DateTimeField(default = False)
#     createdAt = models.DateTimeField(auto_now_add = True)
#     #createdBy = ?
#     #deletedAt = ?
#     #deletedBy = ?