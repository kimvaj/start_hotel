from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SMSSerializer
from .utils import send_sms


class SendSMSView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SMSSerializer(data=request.data)
        if serializer.is_valid():
            to = serializer.validated_data["to"]
            message = serializer.validated_data["message"]
            success, result = send_sms(to, message)
            if success:
                return Response(
                    {"message": "SMS sent successfully", "sid": result},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": result},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
