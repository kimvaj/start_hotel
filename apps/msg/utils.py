# utils.py
import os
from twilio.rest import Client
from django.conf import settings


def send_sms(to, message):
    # Basic phone number validation (you can improve this based on your requirements)
    if not to.startswith("+") or not to[1:].isdigit():
        return False, "Invalid phone number format."

    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        message = client.messages.create(
            body=message, from_=settings.TWILIO_PHONE_NUMBER, to=to
        )
        return True, message.sid
    except Exception as e:
        return False, str(e)
