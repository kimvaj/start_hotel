# apps/hotel/apps.py
from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"

    def ready(self):
        from .models import User
        from django.contrib.auth.models import Group, Permission
        from .signals import reorder_ids_after_change

        for model in [User, Group, Permission]:
            post_delete.connect(reorder_ids_after_change, sender=model)
            post_save.connect(reorder_ids_after_change, sender=model)
