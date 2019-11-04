from django.contrib.auth.models import AbstractUser, User
from django.db import models

""" Override the default representation of user 'username' with 'lastname, firstname""" 
# def get_full_name(self):
#     return self.last_name + ', '+ self.first_name

# User.add_to_class("__str__", get_full_name)
