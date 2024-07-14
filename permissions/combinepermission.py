from rest_framework import permissions

from apps.accounts.models import User


class BaseModelPermissions(permissions.BasePermission):
    model_name = None

    def get_permission_codename(self, action):
        action_permissions = {
            "list": f"view_{self.model_name}",
            "retrieve": f"view_{self.model_name}",
            "create": f"add_{self.model_name}",
            "update": f"change_{self.model_name}",
            "destroy": f"delete_{self.model_name}",
        }
        return action_permissions.get(action)

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        required_permission = self.get_permission_codename(view.action)
        if required_permission:
            return request.user.has_perm(
                f"{self.model_name}.{required_permission}"
            )
        return False


class UserPermissions(BaseModelPermissions):
    model_name = "user"

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if isinstance(obj, User) and obj == request.user:
            return True

        return super().has_permission(request, view)


class HotelPermissions(BaseModelPermissions):
    model_name = "hotel"


class GuestPermissions(BaseModelPermissions):
    model_name = "guest"


class RoomTypePermissions(BaseModelPermissions):
    model_name = "roomtype"


class StaffPermissions(BaseModelPermissions):
    model_name = "staff"

    def has_permission(self, request, view):
        if request.user.groups.filter(name="admin_no_role").exists():
            return view.action in ["list", "retrieve", "destroy", "create"]


class RoomPermissions(BaseModelPermissions):
    model_name = "room"


class BookingPermissions(BaseModelPermissions):
    model_name = "booking"


class PaymentPermissions(BaseModelPermissions):
    model_name = "payment"
