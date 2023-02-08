from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Model(models.Model):
    modelName = models.CharField(max_length = 40)
    magpieModelId = models.IntegerField(unique = True)
    active = models.BooleanField(default = True)
    doi = models.CharField(max_length = 250, blank = True, null = True)
    description = models.TextField(max_length = 4000, blank = True, null = True)

    def __str__(self):
        return '%s' % (self.modelName)

class Dash(models.Model):
    appname = models.CharField(max_length = 2000)

    def __str__(self):
        return '%s' % (self.appname)

class Project(models.Model):
    model = models.ForeignKey(Model, on_delete = models.CASCADE) 
    projectName = models.CharField(max_length = 200)
    magpieProjectId = models.IntegerField(unique = True)
    dash = models.ForeignKey(Dash, on_delete = models.CASCADE, blank = True, null = True)
    description = models.TextField(max_length = 4000, blank = True, null = True)
    
    def __str__(self):
        return '%s' % (self.projectName)

class Prediction(models.Model):
    STATUS = (
        (0, 'started'),
        (1, 'finished'),
        (2, 'failed'),
    )
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    targetId = models.CharField(max_length = 40)
    magpieJobId = models.IntegerField(null=True, default = True)
    status = models.IntegerField(choices = STATUS, default = 0)
    createdAt = models.DateTimeField(auto_now_add = True)
    #createdBy = models.ForeignKey(User, on_delete = models.CASCADE)

