from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class MSGModelViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = response.data
        data["message"] = (
            f"{self.queryset.model.__name__} created successfully."
        )
        return Response(data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = response.data
        data["message"] = (
            f"{self.queryset.model.__name__} updated successfully."
        )
        return Response(data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        data = response.data
        data["message"] = (
            f"{self.queryset.model.__name__} partially updated successfully."
        )
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Response(
            {
                "message": f"{self.queryset.model.__name__} deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT,
        )
