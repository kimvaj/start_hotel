from rest_framework import permissions


class BaseModelPermissions(permissions.BasePermission):
    model = None

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return request.user.has_perm(f"{self.model}.view_{self.model}")
        elif view.action == "create":
            return request.user.has_perm(f"{self.model}.add_{self.model}")
        elif view.action == "update":
            return request.user.has_perm(f"{self.model}.change_{self.model}")
        elif view.action == "destroy":
            return request.user.has_perm(f"{self.model}.delete_{self.model}")
        else:
            return False


class UserPermissions(BaseModelPermissions):
    model = "user"


class HotelPermissions(BaseModelPermissions):
    model = "hotel"


class GuestPermissions(BaseModelPermissions):
    model = "guest"


class RoomTypePermissions(BaseModelPermissions):
    model = "roomtype"


class RoomPermissions(BaseModelPermissions):
    model = "room"


class BookingPermissions(permissions.BasePermission):
    model = "booking"


class PaymentPermissions(BaseModelPermissions):
    model = "payment"
