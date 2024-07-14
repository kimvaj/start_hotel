from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    force_bytes,
    force_str,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address not found.")
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True
    )
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()
            return user
        except DjangoUnicodeDecodeError:
            raise AuthenticationFailed("The reset link is invalid", 401)
        except User.DoesNotExist:
            raise AuthenticationFailed("The user does not exist", 404)
        except Exception as e:
            raise AuthenticationFailed(f"Unexpected error: {str(e)}", 500)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
