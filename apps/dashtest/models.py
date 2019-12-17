from django.db import models

# Create your models here.

class DashSimpleModel(models.Model):
    x = models.IntegerField(default=1)
    y = models.IntegerField(default=1)

    def __str__(self):
        return '%s, %s' % (self.x, self.y)