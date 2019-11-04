from rolepermissions.permissions import register_object_checker
#from predictDemo.roles import SystemAdmin

from django.db.models import Q

@register_object_checker()
def access_trial(role, user, trial):
    if user == trial.createdBy:
        return True
    if trial.trialpermission_set.filter(user=user):
        return True

    return False

@register_object_checker()
def change_trial(role, user, trial):
    if user == trial.createdBy:
        return True
    if trial.trialpermission_set.filter(Q(permission="1") | Q(permission="2") | Q(permission="3"), user=user):
        return True

    return False

@register_object_checker()
def delete_trial(role, user, trial):
    if user == trial.createdBy:
        return True
    if trial.trialpermission_set.filter(Q(permission="2") | Q(permission="3"), user=user):
        return True

    return False

@register_object_checker()
def admin_trial(role, user, trial):
    if user == trial.createdBy:
        return True
    if trial.trialpermission_set.filter(permission="3", user=user):
        return True

    return False

@register_object_checker()
def access_trial_upload(role, user, document):
    from .models import Trial
    trial = document.trial
    if user == trial.createdBy:
        return True
    if trial.trialpermission_set.filter(user=user):
        return True

    return False