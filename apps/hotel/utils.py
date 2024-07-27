from datetime import datetime
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response


def validate_date_range(start_date, end_date):
    today = timezone.now().date()
    if not start_date:
        start_date = today.strftime("%Y-%m-%d")
    if not end_date:
        end_date = today.strftime("%Y-%m-%d")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        return (
            None,
            None,
            Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            ),
        )

    if start_date > end_date:
        return (
            None,
            None,
            Response(
                {"error": "Start date must be before or equal to end date."},
                status=status.HTTP_400_BAD_REQUEST,
            ),
        )

    if start_date > today or end_date > today:
        return (
            None,
            None,
            Response(
                {"error": "Dates cannot be in the future."},
                status=status.HTTP_400_BAD_REQUEST,
            ),
        )

    return start_date, end_date, None
