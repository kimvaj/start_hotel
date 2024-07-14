# apps/hotel/viewsets.py

from rest_framework import status
from rest_framework.response import Response

# from apps.hotel.tasks import create_booking_and_payment
from permissions.permissions import HotelPermissions
from permissions.combinepermission import (
    # BookingPermissions,
    BookingPermissions,
    GuestPermissions,
    PaymentPermissions,
    RoomPermissions,
    RoomTypePermissions,
    StaffPermissions,
)
from common.viewsets.base_viewsets import BaseModelViewSet
from common.viewsets.basecrud import BaseCRUDViewSet
from apps.hotel.models import (
    Hotel,
    Guest,
    Staff,
    RoomType,
    Room,
    Booking,
    Payment,
)
from apps.hotel.serializers import (
    HotelSerializer,
    GuestSerializer,
    StaffSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    BookingSerializer,
    PaymentSerializer,
)


class HotelViewSet(BaseCRUDViewSet, BaseModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [HotelPermissions]


class GuestViewSet(BaseCRUDViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [GuestPermissions]


class StaffViewSet(BaseCRUDViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [StaffPermissions]


class RoomTypeViewSet(BaseCRUDViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [RoomTypePermissions]


class RoomViewSet(BaseCRUDViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [RoomPermissions]

    def create(self, request, *args, **kwargs):
        payment_method = request.data.get(
            "payment_method", Payment.PAYMENT_METHOD_CASH
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.save()  # Save the room instance

        # Now create a booking associated with this room
        booking_data = {
            "guest": request.data.get("guest_id"),
            "room": room.id,
            "check_in_date": request.data.get("check_in_date"),
            "check_out_date": request.data.get("check_out_date"),
            "total_price": request.data.get("total_price"),
        }

        # Enqueue the task
        create_booking_and_payment.delay(booking_data, payment_method)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingViewSet(BaseCRUDViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [BookingPermissions]

    def create(self, request, *args, **kwargs):
        payment_method = request.data.get(
            "payment_method", Payment.PAYMENT_METHOD_CASH
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        booking_data = serializer.validated_data

        # Enqueue the task
        # create_booking_and_payment.delay(booking_data, payment_method)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentViewSet(BaseCRUDViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [PaymentPermissions]
