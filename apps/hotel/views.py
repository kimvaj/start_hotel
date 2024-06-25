from common.viewsets.base_viewsets import BaseModelViewSet
from common.mixins import SoftDeleteMixin
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


class HotelViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class GuestViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class StaffViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class RoomTypeViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer


class RoomViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class BookingViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = RoomType.objects.all()
    serializer_class = BookingSerializer


class PaymentViewSet(BaseModelViewSet, SoftDeleteMixin):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
