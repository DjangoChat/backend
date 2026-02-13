from ....models import UserProfile
from ..serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework import viewsets

class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.active()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    filterset_fields = ["user", "department", "role"]