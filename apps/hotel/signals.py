from django.db.models.signals import (
    post_save,
    pre_save,
    pre_delete,
    post_delete,
)
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from .models import Booking, Room, Payment
from django.db import connection, models


@receiver(post_save, sender=Booking)
def update_room_status_on_booking(sender, instance, created, **kwargs):
    if created:
        # Calculate the total price
        nights = (instance.check_out_date - instance.check_in_date).days
        room_type = instance.room.room_type
        instance.total_price = nights * room_type.price_per_night
        instance.save()

        # Set the room status to 'occupied'
        room = instance.room
        room.status = Room.OCCUPIED
        room.save()


@receiver(pre_save, sender=Booking)
def calculate_total_price_and_check_availability(sender, instance, **kwargs):
    # Calculate the total price
    number_of_nights = (instance.check_out_date - instance.check_in_date).days
    price_per_night = instance.room.room_type.price_per_night
    instance.total_price = number_of_nights * price_per_night

    # Check room availability for new bookings
    if not instance.pk:  # Only check for new bookings
        overlapping_bookings = Booking.objects.filter(
            room=instance.room,
            check_in_date__lt=instance.check_out_date,
            check_out_date__gt=instance.check_in_date,
        )
        if overlapping_bookings.exists():
            raise ValidationError("This room is already booked.")


@receiver(post_save, sender=Booking)
def update_room_status_on_booking(sender, instance, created, **kwargs):
    room = instance.room
    if created:
        room.status = Room.OCCUPIED
    else:
        # Optional: handle updates to existing bookings if needed
        pass
    room.save()


@receiver(post_delete, sender=Booking)
def update_room_status_on_checkout(sender, instance, **kwargs):
    room = instance.room
    room.status = Room.AVAILABLE
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


def reorder_ids(model):
    instances = list(model.objects.all().order_by("id"))
    for i, obj in enumerate(instances, start=1):
        if obj.id != i:
            obj.id = i
            obj.save(update_fields=["id"])

    # Reset the auto-increment field if necessary
    max_id = model.objects.aggregate(max_id=models.Max("id"))["max_id"] or 0
    with connection.cursor() as cursor:
        cursor.execute(
            f"ALTER TABLE {model._meta.db_table} AUTO_INCREMENT = {max_id + 1};"
        )


@receiver(post_delete)
@receiver(post_save)
def reorder_ids_after_change(sender, instance, **kwargs):
    if isinstance(instance, models.Model) and hasattr(instance, "id"):
        reorder_ids(sender)
