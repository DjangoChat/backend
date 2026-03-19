from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle

from ....models import UserProfile
from ....permissions import CustomDjangoModelPermission
from ..serializers import UserProfileSerializer


class UserProfileView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.active()
    serializer_class = UserProfileSerializer
    permission_classes = [CustomDjangoModelPermission]
    throttle_classes = [UserRateThrottle]
    filterset_fields = ["user"]
