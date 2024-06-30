from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from apps.accounts.views import (
    UserViewSet,
    UserRegisterView,
    UserMeView,
    GroupViewSet,
    PermissionViewSet,
    UserTokenObtainPairView,
)
from apps.hotel.views import (
    HotelViewSet,
    GuestViewSet,
    StaffViewSet,
    RoomTypeViewSet,
    RoomViewSet,
    BookingViewSet,
    PaymentViewSet,
)
from apps.resetpwd.views import (
    RequestPasswordResetEmail,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView,
)
from apps.api.views import APIRootView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"permissions", PermissionViewSet)
router.register(r"hotels", HotelViewSet, basename="hotel")
router.register(r"staffs", StaffViewSet, basename="staffs")
router.register(r"guests", GuestViewSet, basename="guest")
router.register(r"room-types", RoomTypeViewSet, basename="room_types")
router.register(r"rooms", RoomViewSet, basename="rooms")
router.register(r"bookings", BookingViewSet, basename="bookings")
router.register(r"payments", PaymentViewSet, basename="payments")

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root-view"),
    path("signin/", UserTokenObtainPairView.as_view(), name="auth-signin"),
    path("register/", UserRegisterView.as_view(), name="auth-register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request_reset_email",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password_token_check",
    ),
    path(
        "password-reset/complete/",
        SetNewPasswordAPIView.as_view(),
        name="set_new_password",
    ),
]

urlpatterns += router.urls
