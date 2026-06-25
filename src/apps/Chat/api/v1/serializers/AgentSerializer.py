from rest_framework import serializers

from apps.Chat.models import Agent, Nature
from apps.Common.models import FeatureCode, AgentType
from .NatureSerializer import ChipNatureSerializer

PERMISSION = {
    AgentType.BASIC: FeatureCode.BASIC_AGENT,
    AgentType.MEDIUM: FeatureCode.MEDIUM_AGENT,
    AgentType.ADVANCE: FeatureCode.ADVANCED_AGENT,
}


class AgentSerializer(serializers.ModelSerializer):
    natures = ChipNatureSerializer(Nature.objects.all())
    has_permission = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            "id",
            "natures",
            "agent_type",
            "has_permission",
        ]

    def get_has_permission(self, obj):
        if (
            self.context["request"]
            .user.get_last_valid_subscription()
            .has_feature(PERMISSION[obj.agent_type])
        ):
            return True
        return False
