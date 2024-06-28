from rest_framework import serializers
from django.utils import timezone
from apps.hotel.models import (
    Hotel,
    Guest,
    Staff,
    Room,
    RoomType,
    Booking,
    Payment,
)


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        def get_sequential_id(self, instance):
            return instance.id


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["total_price"]

    def validate(self, data):
        check_in_date = data.get("check_in_date")
        check_out_date = data.get("check_out_date")
        room = data.get("room")

        if check_in_date and check_out_date <= timezone.now().date():
            raise serializers.ValidationError(
                {
                    "check_out_date": "Check-out date must be after the check-in date."
                }
            )
        if check_in_date and check_in_date < timezone.now().date():
            raise serializers.ValidationError(
                {"check_in_date": "Check-in date cannot be in the past."}
            )
        if room.status == Room.OCCUPIED:
            raise serializers.ValidationError(
                {"room": "This room is already booked."}
            )

        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["amount"]
