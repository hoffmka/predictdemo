##################################
# base file imports roles
##################################

# roles from trials apps
from predictDemo.roles.ttp_domains import *

class admin(AbstractUserRole):
     available_permissions = {
        #'dept_haematology:can_access_data': TRUE,
     }