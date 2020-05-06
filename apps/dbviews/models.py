from django.db import models

# Create your models here.

# Medication

class TreatMedication(models.Model):
    targetId = models.CharField(max_length = 40)
    dateBegin = models.DateField()
    dateEnd = models.DateField(null = True, blank = True)
    interval = models.IntegerField()
    intervalUnit = models.CharField(max_length = 20)
    drugName = models.CharField(max_length = 40)
    dosage = models.IntegerField()
    dosageUnit = models.CharField(max_length = 20)
    medScheme = models.CharField(max_length = 100)
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
    diagType = models.ForeignKey(DiagType, on_delete = models.CASCADE)
    targetId = models.CharField(max_length = 40)
    sampleId = models.CharField(max_length = 40)
    sampleDate = models.DateField()
    parameter = models.ForeignKey(DiagParameter, on_delete = models.CASCADE)
    value = models.CharField(max_length = 100)
    unit = models.CharField(null = True, blank = True, max_length = 20)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now=True)