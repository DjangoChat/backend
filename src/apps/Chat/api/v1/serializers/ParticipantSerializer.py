from rest_framework import serializers

from apps.Chat.models import Participant


class ParticipantSerializer(serializers.ModelSerializer):

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
            "status",
        ]
