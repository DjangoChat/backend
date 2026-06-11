from rest_framework import serializers


class BaseEventSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=[
            "send_message",
            "typing",
            "seen",
            "delete_message",
            "react_message",
        ]
    )


class SendMessageSerializer(serializers.Serializer):
    content = serializers.CharField()


class TypingSerializer(serializers.Serializer):
    is_typing = serializers.BooleanField()


class SeenSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()


class DeleteMessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()


class ReactMessageSerializer(serializers.Serializer):
    message_id = serializers.UUIDField()
    reaction = serializers.CharField()
