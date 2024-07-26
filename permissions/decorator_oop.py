from functools import wraps
from rest_framework import exceptions


def check_permissions(model, actions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(view, request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(view, request, *args, **kwargs)

            action = view.action
            permission_map = {
                "list": f"{model}.view_{model}",
                "retrieve": f"{model}.view_{model}",
                "create": f"{model}.add_{model}",
                "update": f"{model}.change_{model}",
                "destroy": f"{model}.delete_{model}",
            }

            required_permission = permission_map.get(action)

            if required_permission and not request.user.has_perm(
                required_permission
            ):
                raise exceptions.PermissionDenied()

            return view_func(view, request, *args, **kwargs)

        return _wrapped_view

    return decorator


user_permissions = check_permissions(
    "user", ["list", "retrieve", "create", "update", "destroy"]
)
hotel_permissions = check_permissions(
    "hotel", ["list", "retrieve", "create", "update", "destroy"]
)
guest_permissions = check_permissions(
    "guest", ["list", "retrieve", "create", "update", "destroy"]
)
roomtype_permissions = check_permissions(
    "roomtype", ["list", "retrieve", "create", "update", "destroy"]
)
room_permissions = check_permissions(
    "room", ["list", "retrieve", "create", "update", "destroy"]
)
booking_permissions = check_permissions(
    "booking", ["list", "retrieve", "create", "update", "destroy"]
)
payment_permissions = check_permissions(
    "payment", ["list", "retrieve", "create", "update", "destroy"]
)
