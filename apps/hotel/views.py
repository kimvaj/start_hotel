from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from django.utils import timezone
from apps.hotel.utils import validate_date_range
from common.utility.mixins import SoftDeleteMixin
from common.viewsets.basecrud import BaseCRUDViewSet
from common.viewsets.base_viewsets import BaseModelViewSet
from apps.hotel.models import Booking, Payment
from apps.hotel.serializers import BookingSerializer
from rest_framework.exceptions import ValidationError
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


class ReportAPIView(APIView):
    queryset = Booking.objects.all()

    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if not start_date or not end_date:
            raise ValidationError(
                "Both 'start_date' and 'end_date' are required."
            )

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError("Invalid date format. Use 'YYYY-MM-DD'.")

        if start_date > end_date:
            raise ValidationError("'start_date' must be before 'end_date'.")

        bookings = self.queryset.filter(
            check_in_date__gte=start_date, check_out_date__lte=end_date
        )

        report_data = bookings.values(
            "guest__first_name",
            "guest__last_name",
            "room__room_number",
            "check_in_date",
            "check_out_date",
            "total_price",
        )

        # Calculate the total sum of all total_price
        total_sum = (
            bookings.aggregate(total_sum=Sum("total_price"))["total_sum"] or 0
        )

        # Count the number of bookings within the specified range
        booking_count = bookings.count()

        return Response(
            {
                "report": list(report_data),
                "total_bookings": booking_count,
                "total_sum": total_sum,
            },
            status=status.HTTP_200_OK,
        )
