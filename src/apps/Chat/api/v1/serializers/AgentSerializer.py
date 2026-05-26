from rest_framework import serializers
from apps.Chat.models import Agent, Nature
from apps.Common.models import PlanOption


class NatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nature
        fields = [
            "name",
        ]


class AgentSerializer(serializers.ModelSerializer):
    natures = NatureSerializer(read_only=True, many=True)
    has_permission = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            "id",
            "name",
            "description",
            "avatar",
            "natures",
            "agent_type",
            "has_permission",
        ]

    def get_has_permission(self, obj):
        # if PlanOption.PREMIUM in self.context["request"].user.get_active_subscription()
        pass
