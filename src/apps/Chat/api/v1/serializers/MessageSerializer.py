from rest_framework import serializers

from apps.Chat.models import Message


class MessageSerializer(serializers.ModelSerializer):
    seen = serializers.SerializerMethodField()
    me = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "id",
            "me",
            "message_type",
            "content",
            "image",
            "attach",
            "video",
            "sent_at",
            "seen",
        ]

    def get_seen(self, obj):
        return obj.has_been_seen_by_all()

    def get_me(self, obj):
        return self.context["request"].user.id == obj.participant
