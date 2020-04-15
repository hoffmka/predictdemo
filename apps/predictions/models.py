from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Model(models.Model):
    modelName = models.CharField(max_length = 40)
    magpieModelId = models.IntegerField(unique = True)
    active = models.BooleanField(default = True)

    def __str__(self):
        return '%s' % (self.modelName)

class Project(models.Model):
    model = models.ForeignKey(Model, on_delete = models.CASCADE) 
    projectName = models.CharField(max_length = 40)
    magpieProjectId = models.IntegerField(unique = True)

    def __str__(self):
        return '%s' % (self.projectName)

class Prediction(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    targetId = models.CharField(max_length = 40)
    magpieJobId = models.IntegerField(unique = True)
    createdAt = models.DateTimeField(auto_now_add = True)
    #createdBy = models.ForeignKey(User, on_delete = models.CASCADE)