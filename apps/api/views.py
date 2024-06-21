from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse


class APIRootView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "auth": {
                "signin": self.request.build_absolute_uri(
                    reverse("api:auth-signin")
                ),
                "register": self.request.build_absolute_uri(
                    reverse("api:auth-register")
                ),
                "refresh_token": self.request.build_absolute_uri(
                    reverse("api:token_refresh")
                ),
                # Assuming you have an endpoint for 'auth-me'
                # "auth-me": self.request.build_absolute_uri(reverse("api:auth-me")),
            },
            "users": self.request.build_absolute_uri(reverse("api:user-list")),
            "groups": self.request.build_absolute_uri(
                reverse("api:group-list")
            ),
            "permissions": self.request.build_absolute_uri(
                reverse("api:permission-list")
            ),
            "hotels": self.request.build_absolute_uri(
                reverse("api:hotel-list")
            ),
            "guests": self.request.build_absolute_uri(
                reverse("api:guest-list")
            ),
            "staffs": self.request.build_absolute_uri(
                reverse("api:staff-list")
            ),
            "roomtypes": self.request.build_absolute_uri(
                reverse("api:roomtype-list")
            ),
            "rooms": self.request.build_absolute_uri(reverse("api:room-list")),
            "bookings": self.request.build_absolute_uri(
                reverse("api:booking-list")
            ),
            "payments": self.request.build_absolute_uri(
                reverse("api:payment-list")
            ),
        }
        return Response(data)


# 'logout': reverse('api:logout', request=request, format=format),
# 'password_change': reverse('api:password_change', request=request, format=format),
