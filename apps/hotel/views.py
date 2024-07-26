from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from common.utility.mixins import SoftDeleteMixin
from common.viewsets.basecrud import BaseCRUDViewSet
from common.viewsets.base_viewsets import BaseModelViewSet
from apps.hotel.models import Booking, Payment
from apps.hotel.serializers import BookingSerializer
from permissions.combinepermission import BookingPermissions
from weasyprint import HTML

# Import other required models and serializers
from apps.hotel.models import (
    Hotel,
    Guest,
    Staff,
    RoomType,
    Room,
)
from apps.hotel.serializers import (
    HotelSerializer,
    GuestSerializer,
    StaffSerializer,
    RoomTypeSerializer,
    RoomSerializer,
    PaymentSerializer,
)
from permissions.combinepermission import (
    GuestPermissions,
    PaymentPermissions,
    RoomPermissions,
    RoomTypePermissions,
    StaffPermissions,
)
from permissions.permissions import HotelPermissions


class HotelViewSet(BaseCRUDViewSet):
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


class BookingViewSet(SoftDeleteMixin, BaseModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [BookingPermissions]

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

        headers = self.get_success_headers(serializer.data)
        return Response(
            {"msg": "Booking created successfully"},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["get"], url_path="generate-pdf")
    def generate_pdf(self, request, pk=None):
        booking = self.get_object()
        context = {"booking": booking}

        # Ensure the correct template path
        html_string = render_to_string("booking_pdf.html", context)

        # Generate PDF
        pdf_file = HTML(string=html_string).write_pdf()

        # Create HTTP response with PDF
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="booking_{booking.id}.pdf"'
        )

        return response


class PaymentViewSet(SoftDeleteMixin, BaseModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [PaymentPermissions]

    @action(detail=True, methods=["get"], url_path="generate-pdf")
    def generate_pdf(self, request, pk=None):
        payment = self.get_object()
        context = {"payment": payment}

        # Render the HTML template with payment context
        html_string = render_to_string("payment_pdf.html", context)

        # Generate PDF
        pdf_file = HTML(string=html_string).write_pdf()

        # Create HTTP response with PDF
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="payment_{payment.id}.pdf"'
        )

        return response
