from rest_framework import generics
from rest_framework.throttling import UserRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.Chat.models import Agent
from apps.Chat.api.v1.serializers import AgentSerializer
from apps.Authorization.permissions import CustomPermission, SubscriptionPermission


class AgentView(generics.ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    throttle_classes = [UserRateThrottle]
    filterset_fields = ["agent_type", "natures__name"]

    @extend_schema(
        tags=["Chat"],
        summary="List available agents",
        description=(
            "Retrieves a list of all available chat agents with optional filtering. "
            "Can filter by agent_type and natures__name. "
            "Requires subscription and proper permissions."
        ),
        responses={
            200: OpenApiResponse(
                response=AgentSerializer(many=True),
                description="List of agents retrieved successfully",
            )
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
