from common.utility.mixins import SoftDeleteMixin
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from common.viewsets.base_viewsets import BaseModelViewSet


class BaseCRUDViewSet(SoftDeleteMixin, BaseModelViewSet):
    def get_object(self, pk):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=pk)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
