from django.db import connection, models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


def reorder_ids(model):
    # Get all instances ordered by id
    instances = list(model.objects.all().order_by("id"))

    with connection.cursor() as cursor:
        for i, obj in enumerate(instances, start=1):
            if obj.id != i:
                # Update the ID using raw SQL
                cursor.execute(
                    f"UPDATE {model._meta.db_table} SET id = %s WHERE id = %s",
                    [i, obj.id],
                )

        # Reset the auto-increment field if necessary
        max_id = len(instances)
        cursor.execute(
            f"ALTER TABLE {model._meta.db_table} AUTO_INCREMENT = %s",
            [max_id + 1],
        )


@receiver(post_delete)
@receiver(post_save)
def reorder_ids_after_change(sender, instance, **kwargs):
    # Check if the sender is a model we want to reorder
    if isinstance(instance, models.Model) and hasattr(instance, "id"):
        reorder_ids(sender)
