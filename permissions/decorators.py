from functools import wraps
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import Group

def user_is_admin(view_func):
    @wraps(view_func)
    def _wrapped_view(viewset, request, *args, **kwargs):
        if request.user.groups.filter(name='admin').exists():
            return view_func(viewset, request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to perform this action.")
    return _wrapped_view

def user_is_staff(view_func):
    @wraps(view_func)
    def _wrapped_view(viewset, request, *args, **kwargs):
        if request.user.groups.filter(name='staff').exists():
            return view_func(viewset, request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to perform this action.")
    return _wrapped_view

def user_is_superadmin(view_func):
    @wraps(view_func)
    def _wrapped_view(viewset, request, *args, **kwargs):
        if request.user.groups.filter(name='superadmin').exists():
            return view_func(viewset, request, *args, **kwargs)
        else:
            raise PermissionDenied("You do not have permission to perform this action.")
    return _wrapped_view
