# apps/hotel/handlers.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils import timezone


@receiver(post_migrate)
def schedule_tasks(sender, **kwargs):
    schedule, created = CrontabSchedule.objects.get_or_create(
        minute="*/1",  # every minute for testing purposes
        hour="*",
        day_of_week="*",
        day_of_month="*",
        month_of_year="*",
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name="Update room statuses",
        task="apps.hotel.tasks.update_room_statuses",
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name="Check booking payments",
        task="apps.hotel.tasks.check_booking_payments",
    )
