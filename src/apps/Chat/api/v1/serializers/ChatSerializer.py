from rest_framework import serializers


class StartChatSerializerInput(serializers.Serializer):
    participant_id = serializers.UUIDField()


class StartChatSerializerResponseOutput(serializers.Serializer):
    chat_id = serializers.UUIDField()
    created = serializers.BooleanField()
