# core/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.prod")

# Create a Celery instance
app = Celery("core")

# Using the Celery configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True
# Optionally configure other Celery settings here
app.conf.worker_prefetch_multiplier = 1
app.conf.task_acks_late = True
