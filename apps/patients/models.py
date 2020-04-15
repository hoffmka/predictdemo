from django.contrib.auth.models import User
from django.db import models
# from .. trials.models import *

class Model(models.Model):
    name = models.CharField(max_length = 40)

    def __str__(self):
        return '%s' % (self.name)

class Prediction(models.Model):
    targetId = models.CharField(max_length = 40)
    model = models.ForeignKey(Model, on_delete = models.CASCADE)
    magpieProjectId = models.IntegerField()
    magpieJobId = models.IntegerField(unique = True)
    createdAt = models.DateTimeField(auto_now_add = True)
    createdBy = models.ForeignKey(User, on_delete = models.CASCADE)