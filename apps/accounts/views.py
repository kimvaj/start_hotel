from rest_framework import status
from rest_framework.decorators import APIView, action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Group, Permission
from django.http import Http404
from .models import User
from .serializers import (
    LogoutSerializer,
    RefreshTokenSerializer,
    UserSerializer,
    GroupSerializer,
    PermissionSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt
from django.conf import settings
from django.http import Http404
from drf_yasg import openapi
from rest_framework.authentication import TokenAuthentication

from drf_yasg.utils import swagger_auto_schema
from .models import User
from .serializers import (
    EmailVerificationSerializer,
    # LogoutSerializer,
    UserTokenObtainPairSerializer,
    UserRegisterSerializer,
    UserSerializer,
)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.action in ["restore", "hard_delete"]:
            return User.all_objects.all()
        return User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def _get_user_or_404(self, pk):
        try:
            user = User.all_objects.get(pk=pk)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404("User not found")

    @action(detail=False, methods=["get"], url_path="soft-delete")
    def soft_delete(self, request):
        deleted_users = User.deleted_objects.all()
        page = self.paginate_queryset(deleted_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(deleted_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, pk=None):
        user = self._get_user_or_404(pk)
        if user.is_deleted:
            user.restore()
            return Response(
                {"status": "user restored"}, status=status.HTTP_200_OK
            )
        return Response(
            {"status": "user is not deleted"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["delete"], url_path="hard-delete")
    def hard_delete(self, request, pk=None):
        user = self._get_user_or_404(pk)
        user.hard_delete()
        return Response(
            {"status": "user permanently deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            response.data["user_id"] = user.id
            response.data["email"] = user.email
        return response


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer


class UserMeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyEmail(APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="Description",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload["user_id"])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response(
                {"email": "Successfully activated"}, status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation Expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"msg": "logout successfully"}, status=status.HTTP_204_NO_CONTENT
        )
