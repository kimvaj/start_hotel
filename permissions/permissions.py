from rest_framework import permissions

from apps.accounts.models import User


class HasAnyPermission(permissions.BasePermission):
    def __init__(self, required_permissions):
        self.required_permissions = required_permissions

    def has_permission(self, request, view):
        return any(
            request.user.has_perm(permission)
            for permission in self.required_permissions
        )


class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow superusers
        if request.user.is_superuser:
            return True

        # Allow users to perform actions on their own user record
        if isinstance(obj, User) and obj == request.user:
            return True
        action_permissions = {
            "list": "view_user",
            "retrieve": "view_user",
            "create": "add_user",
            "update": "change_user",
            "destroy": "delete_user",
        }
        required_permission = action_permissions.get(view.action)
        if required_permission:
            return request.user.groups.filter(
                permissions__codename=required_permission
            ).exists()
        return False


class HotelPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return request.user.has_perm("hotel.view_hotel")
        elif view.action == "create":
            return request.user.has_perm("hotel.add_hotel")
        elif view.action == "update":
            return request.user.has_perm("hotel.change_hotel")
        elif view.action == "destroy":
            return request.user.has_perm("hotel.delete_hotel")
        else:
            return False


class GuestPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return request.user.has_perm("guest.view_guest")
        elif view.action == "create":
            return request.user.has_perm("guest.add_guest")
        elif view.action == "update":
            return request.user.has_perm("guest.change_guest")
        elif view.action == "destroy":
            return request.user.has_perm("guest.delete_guest")
        else:
            return False


class RoomTypePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return request.user.has_perm("roomtype.view_roomtype")
        elif view.action == "create":
            return request.user.has_perm("roomtype.add_roomtype")
        elif view.action == "update":
            return request.user.has_perm("roomtype.change_roomtype")
        elif view.action == "destroy":
            return request.user.has_perm("roomtype.delete_roomtype")
        else:
            return False


class RoomPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return request.user.has_perm("room.view_room")
        elif view.action == "create":
            return request.user.has_perm("room.add_room")
        elif view.action == "update":
            return request.user.has_perm("room.change_room")
        elif view.action == "destroy":
            return request.user.has_perm("room.delete_room")
        else:
            return False


class BookingPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user:
            return view.action in ["list", "retrieve", "destroy", "create"]
        if view.action in ["list", "retrieve"]:
            return request.user.has_perm("booking.view_booking")
        elif view.action == "create":
            return request.user.has_perm("booking.add_booking")
        elif view.action == "update":
            return request.user.has_perm("booking.change_hotel")
        elif view.action == "destroy":
            return request.user.has_perm("booking.delete_hotel")
        else:
            return False


class PaymenPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if view.action in ["list", "retrieve"]:
            return request.user.has_perm("payment.view_payment")
        elif view.action == "create":
            return request.user.has_perm("payment.add")
        elif view.action == "update":
            return request.user.has_perm("payment.change_payment")
        elif view.action == "destroy":
            return request.user.has_perm("payment.delete_payment")
        else:
            return False
