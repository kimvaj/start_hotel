from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from django.urls import path
from rest_framework.routers import DefaultRouter
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
from apps.api.views import APIRootView


app_name = "api"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"permissions", PermissionViewSet)
router.register(r"hotels", HotelViewSet)
router.register(r"guests", GuestViewSet)
router.register(r"staffs", StaffViewSet)
router.register(r"roomtypes", RoomTypeViewSet)
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"bookings", BookingViewSet, basename="booking")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root-view"),
    # path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(
        "auth/signin/", UserTokenObtainPairView.as_view(), name="auth-signin"
    ),
    path("auth/register/", UserRegisterView.as_view(), name="auth-register"),
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]

urlpatterns += router.urls
