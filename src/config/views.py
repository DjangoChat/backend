from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        health_status = {
            "status": "healthy",
            "services": {"database": "unhealthy", "cache": "unhealthy"},
        }

        return Response(health_status, status=status.HTTP_200_OK)
