from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.exceptions import MaxRetriesExceededError


@shared_task(bind=True, max_retries=3, default_retry_delay=20)
def send_reset_password_email(self, email_body, to_email, email_subject):
    try:
        send_mail(
            email_subject,
            email_body,
            settings.DEFAULT_FROM_EMAIL,
            [to_email],
            fail_silently=False,
        )
    except Exception as exc:
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            pass
