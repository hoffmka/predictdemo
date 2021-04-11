from django.contrib.auth.models import AbstractUser, User, Group
from django.db import models

""" Override the default representation of user 'username' with 'lastname, firstname""" 
# def get_full_name(self):
#     return self.last_name + ', '+ self.first_name

# User.add_to_class("__str__", get_full_name)


'''Adding additional fields to group'''
Group.add_to_class('description', models.CharField(max_length=180,null=True, blank=True))
Group.add_to_class('ttp_studyId', models.CharField(max_length=180,null=True, blank=True))
Group.add_to_class('ttp_targetIdType', models.CharField(max_length=180,null=True, blank=True))