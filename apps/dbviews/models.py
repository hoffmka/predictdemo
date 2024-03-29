from django.db import models
from ..trials.models import Trial
# Create your models here.

# Medication

class PatientTrial(models.Model):
    GENDER = (
        ('male', 'male'),
        ('female', 'female')
    )
    trial = models.ForeignKey(Trial, on_delete = models.PROTECT, null = True, blank = True)
    targetId = models.CharField(max_length = 40)
    gender = models.CharField(choices=GENDER, max_length = 10, null=True, blank=True)

class TreatMedication(models.Model):
    trial = models.ForeignKey(Trial, on_delete = models.PROTECT, null = True, blank = True)
    targetId = models.CharField(max_length = 40)
    dateBegin = models.DateField()
    dateEnd = models.DateField(null = True, blank = True)
    interval = models.IntegerField(null = True, blank = True)
    intervalUnit = models.CharField(max_length = 20, null = True, blank = True)
    drugName = models.CharField(max_length = 40, null = True, blank = True)
    dosage = models.IntegerField(null = True, blank = True)
    dosageUnit = models.CharField(max_length = 20, null = True, blank = True)
    medScheme = models.CharField(max_length = 100, null = True, blank = True)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now=True)

class DiagType(models.Model):
    diagTypeName = models.CharField(max_length = 100)

    def __str__(self):
        return '%s' % (self.diagTypeName)

class DiagParameter(models.Model):
    parameterName = models.CharField(max_length = 100)

    def __str__(self):
        return '%s' % (self.parameterName)
        
class Diagnostic(models.Model):
    diagType = models.ForeignKey(DiagType, on_delete = models.PROTECT)
    trial = models.ForeignKey(Trial, on_delete = models.PROTECT, null = True, blank = True)
    targetId = models.CharField(max_length = 40)
    sampleId = models.CharField(max_length = 40)
    sampleDate = models.DateField()
    parameter = models.ForeignKey(DiagParameter, on_delete = models.CASCADE)
    value = models.CharField(max_length = 100, null = True, blank = True)
    unit = models.CharField(null = True, blank = True, max_length = 20)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now=True)