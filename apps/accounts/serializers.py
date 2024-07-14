from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from django.conf import settings

from django.contrib import auth
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
import jwt


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "name", "codename")


class GroupSerializer(serializers.ModelSerializer):
    # permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name", "permissions")


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the payload (not the token itself)
        token["user_id"] = user.id
        token["email"] = user.email
        # ...

        return token


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups')
        fields = "__all__"
        extra_kwargs = {
            "last_login": {"required": False},
            "date_joined": {"required": False},
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        # Validate the new password using Django's password validation
        validate_password(value)
        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data["password"] = make_password(validated_data["password"])

        # Set is_active to True
        validated_data["is_active"] = True

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Remove password from validated_data to prevent updating it
        validated_data.pop("password", None)
        return super().update(instance, validated_data)

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        # If this is an update operation, remove the password field
        if self.instance:
            fields.pop("password")

        # If the user has the permission to modify the 'is_superuser' field
        # Otherwise, hide the 'is_superuser' field
        if request and request.method in ["POST", "PUT", "PATCH"]:
            user = request.user

            if (
                not user.is_superuser
                and not user.groups.filter(
                    permissions__codename="change_is_superuser"
                ).exists()
            ):
                fields.pop("is_staff")
                fields.pop("is_superuser")

        return fields


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if (
            filtered_user_by_email.exists()
            and filtered_user_by_email[0].auth_provider != "email"
        ):
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {
            "email": user.email,
            "username": user.username,
            "tokens": user.tokens,
        }

        return super().validate(attrs)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": _("Token is invalid or expired")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {"bad_token": "Token is expired or invalid"}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
