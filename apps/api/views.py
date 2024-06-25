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
                # Add 'auth-me' endpoint if it exists
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
        }
        return Response(data)
