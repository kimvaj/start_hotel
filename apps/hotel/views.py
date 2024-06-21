from rest_framework import permissions, viewsets
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


class HotelViewSet(viewsets.ModelViewSet):

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class GuestViewSet(viewsets.ModelViewSet):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class StaffViewSet(viewsets.ModelViewSet):

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class RoomTypeViewSet(viewsets.ModelViewSet):

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomViewSet(viewsets.ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(viewsets.ModelViewSet):

    queryset = RoomType.objects.all()
    serializer_class = BookingSerializer


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
