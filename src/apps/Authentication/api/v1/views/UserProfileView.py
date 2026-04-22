from rest_framework import viewsets
from rest_framework.throttling import UserRateThrottle

from ....models import UserProfile
from ..serializers import UserProfileSerializer

from apps.Common.models import CustomGroups
from apps.Authorization.permissions import CustomPermission


class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [CustomPermission]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        user = self.request.user

        if self.action == "list":
            if CustomGroups.ADMIN in user.groups:
                return UserProfile.objects.active()
            return UserProfile.objects.none()

        return UserProfile.objects.all()
