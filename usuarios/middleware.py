from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin


class RestrictStaffToAdminMiddleware(MiddlewareMixin):
    """
    A middleware that restricts staff members access to administration panels.
    """

    def process_request(self, request):
        if request.user.is_staff and not request.user.is_superuser:
            if request.path.startswith(reverse('admin:index')):
                msg = u'Staff members cannot access the public site.'
                return HttpResponseForbidden(msg)