# apps/hotel/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Room, Booking

@shared_task
def update_room_statuses():
    today = timezone.now().date()
    # Find bookings that have ended
    ended_bookings = Booking.objects.filter(check_out_date__lt=today, room__status=Room.OCCUPIED)
    for booking in ended_bookings:
        room = booking.room
        room.status = Room.AVAILABLE
        room.save()

@shared_task
def check_booking_payments():
    for booking in Booking.objects.all():
        total_paid = sum(payment.amount for payment in booking.payment_booking.all())
        if total_paid >= booking.total_price:
            booking.status = 'paid'
        else:
            booking.status = 'unpaid'
        booking.save()
