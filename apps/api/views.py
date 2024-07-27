from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse
from apps.accounts.views import UserTokenObtainPairView, UserRegisterView
from apps.resetpwd.views import (
    RequestPasswordResetEmail,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.accounts.views import UserViewSet, GroupViewSet, PermissionViewSet
from apps.hotel.views import (
    HotelViewSet,
    GuestViewSet,
    StaffViewSet,
    RoomTypeViewSet,
    RoomViewSet,
    BookingViewSet,
    PaymentViewSet,
)
from rest_framework.routers import DefaultRouter


class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "auth": {
                "signin": self.request.build_absolute_uri(
                    reverse("api:auth-signin")
                ),
                "logout": self.request.build_absolute_uri(
                    reverse("api:logout")
                ),
                "register": self.request.build_absolute_uri(
                    reverse("api:auth-register")
                ),
                "verify-email": self.request.build_absolute_uri(
                    reverse("api:email-verify")
                ),
                "refresh_token": self.request.build_absolute_uri(
                    reverse("api:token_refresh")
                ),
                "auth-me": self.request.build_absolute_uri(
                    reverse("api:auth-me")
                ),
            },
            "pwd": {
                "request-reset-email": self.request.build_absolute_uri(
                    reverse("api:request_reset_email")
                ),
                "password-reset-confirm": self.request.build_absolute_uri(
                    reverse(
                        "api:password_token_check",
                        kwargs={"uidb64": "uid", "token": "token"},
                    )
                ),
                "set_new_password": self.request.build_absolute_uri(
                    reverse("api:set_new_password")
                ),
                "change_password": self.request.build_absolute_uri(
                    reverse("api:change-password")
                ),
            },
            "User": {
                "users": self.request.build_absolute_uri(
                    reverse("api:user-list")
                ),
                "groups": self.request.build_absolute_uri(
                    reverse("api:group-list")
                ),
                "permissions": self.request.build_absolute_uri(
                    reverse("api:permission-list")
                ),
            },
            "hotels": {
                "hotels": self.request.build_absolute_uri(
                    reverse("api:hotel-list")
                ),
                "staffs": self.request.build_absolute_uri(
                    reverse("api:staffs-list")
                ),
                "guests": self.request.build_absolute_uri(
                    reverse("api:guest-list")
                ),
                "room_types": self.request.build_absolute_uri(
                    reverse("api:room_types-list")
                ),
                "rooms": self.request.build_absolute_uri(
                    reverse("api:rooms-list")
                ),
                "bookings": self.request.build_absolute_uri(
                    reverse("api:bookings-list")
                ),
                "payments": self.request.build_absolute_uri(
                    reverse("api:payments-list")
                ),
                "reports": self.request.build_absolute_uri(
                    reverse("api:report")
                ),
            },
        }
        return Response(data)
