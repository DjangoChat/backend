from rest_framework import generics
from rest_framework.throttling import UserRateThrottle

from apps.Chat.models import Agent
from apps.Chat.api.v1.serializers import AgentSerializer
from apps.Authorization.permissions import CustomPermission, SubscriptionPermission


class AgentView(generics.ListAPIView):
    query_set = Agent.objects.all()
    serializer = AgentSerializer
    permission_classes = [SubscriptionPermission, CustomPermission]
    throttle_classes = [UserRateThrottle]
    filterset_fields = ["agent_type", "natures__name"]
