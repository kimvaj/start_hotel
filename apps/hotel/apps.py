# apps/hotel/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class HotelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.hotel"

    def ready(self):
        from .models import (
            Hotel,
            Staff,
            Guest,
            RoomType,
            Room,
            Booking,
            Payment,
        )
        from .signals import reorder_ids_after_change

        for model in [Hotel, Staff, Guest, RoomType, Room, Booking, Payment]:
            post_delete.connect(reorder_ids_after_change, sender=model)
            post_save.connect(reorder_ids_after_change, sender=model)
