from functools import wraps
from rest_framework import status
from rest_framework.response import Response
from apps.accounts.models import User


def has_any_permission(required_permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not any(
                request.user.has_perm(permission)
                for permission in required_permissions
            ):
                return Response(
                    {"detail": "Permission denied."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def user_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        obj = kwargs.get("pk")
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        if isinstance(obj, User) and obj == request.user:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "view_user",
            "retrieve": "view_user",
            "create": "add_user",
            "update": "change_user",
            "destroy": "delete_user",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if (
            required_permission
            and request.user.groups.filter(
                permissions__codename=required_permission
            ).exists()
        ):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view


def hotel_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "hotel.view_hotel",
            "retrieve": "hotel.view_hotel",
            "create": "hotel.add_hotel",
            "update": "hotel.change_hotel",
            "destroy": "hotel.delete_hotel",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if required_permission and request.user.has_perm(required_permission):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view


def guest_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "guest.view_guest",
            "retrieve": "guest.view_guest",
            "create": "guest.add_guest",
            "update": "guest.change_guest",
            "destroy": "guest.delete_guest",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if required_permission and request.user.has_perm(required_permission):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view


def room_type_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "roomtype.view_roomtype",
            "retrieve": "roomtype.view_roomtype",
            "create": "roomtype.add_roomtype",
            "update": "roomtype.change_roomtype",
            "destroy": "roomtype.delete_roomtype",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if required_permission and request.user.has_perm(required_permission):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view


def room_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "room.view_room",
            "retrieve": "room.view_room",
            "create": "room.add_room",
            "update": "room.change_room",
            "destroy": "room.delete_room",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if required_permission and request.user.has_perm(required_permission):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view


def booking_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "booking.view_booking",
            "retrieve": "booking.view_booking",
            "create": "booking.add_booking",
            "update": "booking.change_booking",
            "destroy": "booking.delete_booking",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if required_permission and request.user.has_perm(required_permission):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view


def payment_permissions(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        action_permissions = {
            "list": "payment.view_payment",
            "retrieve": "payment.view_payment",
            "create": "payment.add_payment",
            "update": "payment.change_payment",
            "destroy": "payment.delete_payment",
        }
        required_permission = action_permissions.get(view_func.__name__)
        if required_permission and request.user.has_perm(required_permission):
            return view_func(request, *args, **kwargs)

        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    return _wrapped_view
