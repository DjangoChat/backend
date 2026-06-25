from rest_framework import serializers

from apps.Chat.models import Participant
from .AgentSerializer import AgentSerializer


class ParticipantSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = [
            "id",
            "user",
            "agent",
            "first_name",
            "last_name",
            "nickname",
            "avatar",
            "participant_status",
            "details",
        ]

    def get_details(self, obj):
        if obj.agent:
            return AgentSerializer(obj.agent).data
        return None
