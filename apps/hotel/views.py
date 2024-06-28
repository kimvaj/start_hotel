from common.viewsets.base_viewsets import BaseModelViewSet
from common.mixins import SoftDeleteMixin
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
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


class HotelViewSet(BaseCRUDViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class GuestViewSet(BaseCRUDViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class StaffViewSet(BaseCRUDViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class RoomTypeViewSet(BaseCRUDViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomViewSet(BaseCRUDViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def create(self, request, *args, **kwargs):
        payment_method = request.data.get("payment_method", Payment.PAYMENT_METHOD_CASH)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.save()  # Save the room instance

        # Now create a booking associated with this room
        booking_data = {
            "guest": request.data.get("guest_id"),  # Assuming you provide guest_id in request data
            "room": room.id,
            "check_in_date": request.data.get("check_in_date"),
            "check_out_date": request.data.get("check_out_date"),
        }

        booking_serializer = BookingSerializer(data=booking_data)
        booking_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            booking_instance = booking_serializer.save()

            # Create payment upon successful booking
            Payment.objects.create(
                booking=booking_instance,
                amount=booking_instance.total_price,
                payment_date=timezone.now(),
                payment_method=payment_method,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BookingViewSet(BaseCRUDViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        payment_method = request.data.get(
            "payment_method", Payment.PAYMENT_METHOD_CASH
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            self.perform_create(serializer)
            instance = serializer.instance

            # Create payment upon successful booking
            Payment.objects.create(
                booking=instance,
                amount=instance.total_price,
                payment_date=timezone.now(),
                payment_method=payment_method,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentViewSet(BaseCRUDViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
