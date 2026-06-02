from rest_framework import generics
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.Chat.models import Nature
from apps.Chat.api.v1.serializers import DropdownNatureSerializer
from apps.Authorization.permissions import CustomPermission, SubscriptionPermission


class NatureDropDownView(generics.ListAPIView):
    queryset = Nature.objects.all()
    serializer_class = DropdownNatureSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    throttle_classes = [UserRateThrottle]
    pagination_class = None

    @extend_schema(
        tags=["Chat"],
        summary="List nature options",
        description=(
            "Retrieves a list of all available nature/chat types. "
            "Requires subscription and proper permissions. "
            "No pagination applied."
        ),
        responses={
            200: OpenApiResponse(
                response=DropdownNatureSerializer(many=True),
                description="List of nature options retrieved successfully",
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
