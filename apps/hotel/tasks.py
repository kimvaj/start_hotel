# # apps/hotel/tasks.py

# from celery import shared_task
# from rest_framework.exceptions import ValidationError
# from apps.hotel.models import Booking, Payment
# from apps.hotel.serializers import BookingSerializer
# from django.utils import timezone
# from django.db import transaction


# @shared_task
# def create_booking_and_payment(booking_data, payment_method):
#     serializer = BookingSerializer(data=booking_data)
#     if not serializer.is_valid():
#         raise ValidationError(serializer.errors)

#     with transaction.atomic():
#         booking_instance = serializer.save()
#         Payment.objects.create(
#             booking=booking_instance,
#             amount=booking_instance.total_price,
#             payment_date=timezone.now(),
#             payment_method=payment_method,
#         )
