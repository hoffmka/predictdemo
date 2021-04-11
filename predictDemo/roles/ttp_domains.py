from rolepermissions.roles import AbstractUserRole

class dept_haematology(AbstractUserRole):
     available_permissions = {
        #'dept_haematology:can_access_data': TRUE,
     }

class trial_cml(AbstractUserRole):
     available_permissions = {
        #'dept_haematology:can_access_data': TRUE,
     }