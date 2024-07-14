# serializers.py

from rest_framework import serializers


class SMSSerializer(serializers.Serializer):
    to = serializers.CharField(max_length=15)
    message = serializers.CharField(max_length=160)
