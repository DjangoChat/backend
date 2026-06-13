from rest_framework import serializers

from apps.Chat.models import Chat


class StartChatSerializerInput(serializers.Serializer):
    participant_id = serializers.UUIDField()


class StartChatSerializerResponseOutput(serializers.Serializer):
    chat_id = serializers.UUIDField()
    created = serializers.BooleanField()


class SimpleChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = "__all__"
