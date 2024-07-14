from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Hotel, Staff, Guest, RoomType, Room, Booking, Payment


class BookingModelTest(TestCase):
    def setUp(self):
        # Create test data
        self.hotel = Hotel.objects.create(
            name="Test Hotel",
            address="Test Address",
            village="Test Village",
            district="Test District",
            province="Test Province",
            phone="123456789",
            email="test@example.com",
            stars=4,
            check_in_time="14:00:00",
            check_out_time="12:00:00",
        )

        self.guest = Guest.objects.create(
            first_name="John",
            last_name="Doe",
            date_of_birth="1990-01-01",
            email="john.doe@example.com",
            phone="987654321",
            address="Test Address",
        )

        self.room_type = RoomType.objects.create(
            name="Single Room",
            description="Single bed",
            price_per_night=50.00,
            capacity=1,
        )

        self.room = Room.objects.create(
            hotel=self.hotel,
            room_type=self.room_type,
            room_number="101",
            status=Room.AVAILABLE,
            image="room_images/101.jpg",
        )

    def test_booking_valid(self):
        # Create a valid booking instance
        booking = Booking.objects.create(
            guest=self.guest,
            room=self.room,
            check_in_date=timezone.now().date(),
            check_out_date=timezone.now().date() + timezone.timedelta(days=1),
            total_price=100.00,
        )

        self.assertEqual(booking.check_out_date > booking.check_in_date, True)

    def test_booking_invalid_check_in_date(self):
        # Attempt to create a booking with a past check-in date
        with self.assertRaises(ValidationError):
            Booking.objects.create(
                guest=self.guest,
                room=self.room,
                check_in_date=timezone.now().date()
                - timezone.timedelta(days=1),
                check_out_date=timezone.now().date()
                + timezone.timedelta(days=1),
                total_price=100.00,
            )

    def test_booking_invalid_check_out_date(self):
        # Attempt to create a booking with check-out date before check-in date
        with self.assertRaises(ValidationError):
            Booking.objects.create(
                guest=self.guest,
                room=self.room,
                check_in_date=timezone.now().date(),
                check_out_date=timezone.now().date(),
                total_price=100.00,
            )
