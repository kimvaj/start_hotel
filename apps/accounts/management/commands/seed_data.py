from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = "Seed initial data for users"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        # Option 1: Force seeding regardless of existing users
        # Comment out or remove this block to always seed
        if User.objects.exists():
            self.stdout.write(
                self.style.NOTICE(
                    "Your actions are done, please check in your database"
                )
            )
            # You may choose to return here if you want to skip the seeding
            # return

        # Create initial user(s)
        try:
            user_data = {
                "email": "adfafdseww@example.com",
                "first_name": "wafafork",
                "last_name": "vdafang",
                "password": "admin123#@@",
                "is_staff": True,
                "is_superuser": True,
            }
            user = User.objects.create_superuser(**user_data)

            # Assign user to a specific group
            group, created = Group.objects.get_or_create(name="admin")
            user.groups.add(group)

            self.stdout.write(
                self.style.SUCCESS("Successfully seeded superuser data.")
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(
                    "Failed to seed superuser data: {}".format(str(e))
                )
            )
