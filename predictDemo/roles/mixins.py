from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.conf import settings

from rolepermissions.checkers import has_object_permission


class HasObjectPermissionMixin(object):
    checker_name = ''

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            self.object = self.get_object()
            if has_object_permission(self.checker_name, request.user, self.object):
                return super().dispatch(request, *args, **kwargs)

        if hasattr(settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN'):
            return redirect_to_login(request.get_full_path())

        raise PermissionDenied