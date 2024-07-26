from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    model_name = ""

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        action_permissions = {
            "list": f"{self.model_name}.view_{self.model_name}",
            "retrieve": f"{self.model_name}.view_{self.model_name}",
            "create": f"{self.model_name}.add_{self.model_name}",
            "update": f"{self.model_name}.change_{self.model_name}",
            "destroy": f"{self.model_name}.delete_{self.model_name}",
        }

        permission = action_permissions.get(view.action)
        return request.user.has_perm(permission) if permission else False


class UserPermissions(BasePermission):
    model_name = "user"


class HotelPermissions(BasePermission):
    model_name = "hotel"


class GuestPermissions(BasePermission):
    model_name = "guest"


class RoomTypePermissions(BasePermission):
    model_name = "roomtype"


class RoomPermissions(BasePermission):
    model_name = "room"


class BookingPermissions(BasePermission):
    model_name = "booking"


class PaymentPermissions(BasePermission):
    model_name = "payment"


class StaffPermissions(BasePermission):
    model_name = "staff"
