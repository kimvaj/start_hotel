from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking, Room, Payment


@receiver(pre_save, sender=Booking)
def calculate_total_price(sender, instance, **kwargs):
    number_of_nights = (instance.check_out_date - instance.check_in_date).days
    price_per_night = instance.room.room_type.price_per_night
    instance.total_price = number_of_nights * price_per_night


@receiver(pre_save, sender=Booking)
def check_room_availability(sender, instance, **kwargs):
    if instance.pk:
        return
    overlapping_bookings = Booking.objects.filter(
        room=instance.room,
        check_in_date__lt=instance.check_out_date,
        check_out_date__gt=instance.check_in_date,
    )
    if overlapping_bookings.exists():
        raise ValidationError(
            "This room is already booked for the selected dates."
        )


@receiver(post_save, sender=Booking)
def update_room_status_on_booking(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        room.status = Room.OCCUPIED
        room.save()


@receiver(pre_delete, sender=Booking)
def update_room_status_on_booking_deletion(sender, instance, **kwargs):
    room = instance.room
    room.status = Room.AVAILABLE
    room.save()


@receiver(post_save, sender=Payment)
def update_booking_payment_status(sender, instance, created, **kwargs):
    booking = instance.booking
    total_paid = sum(
        payment.amount for payment in booking.payment_booking.all()
    )
    if total_paid >= booking.total_price:
        booking.status = "paid"
    else:
        booking.status = "unpaid"
    booking.save()
