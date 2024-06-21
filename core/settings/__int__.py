from __future__ import absolute_import, unicode_literals
from dotenv import load_dotenv
import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from ..celery import app as celery_app
load_dotenv()

__all__ = ('celery_app',)




# Set default DJANGO_ENV to 'dev' if not specified in .env
DJANGO_ENV = os.getenv("DJANGO_ENV", "prod")

if DJANGO_ENV == "prod":
    from .prod import *
else:
    from .dev import *
