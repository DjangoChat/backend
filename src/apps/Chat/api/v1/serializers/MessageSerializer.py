from rest_framework import serializers

from apps.Chat.models import Message


class MessageDetailedSerializer(serializers.ModelSerializer):
    seen = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "participant",
            "message_type",
            "content",
            "image",
            "attach",
            "video",
            "sent_at",
            "seen",
        ]

    def get_seen(self, obj):
        request = self.context.get("request")

        if request is None:
            return None

        participant = request.user.participant

        if obj.participant == participant:
            return obj.has_been_seen_by_all()

        return None


class MessageSerializer(serializers.ModelSerializer):
    participant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "chat",
            "participant",
            "message_type",
            "content",
            "image",
            "attach",
            "video",
        ]
