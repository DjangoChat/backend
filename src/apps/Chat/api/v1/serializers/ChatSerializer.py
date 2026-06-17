from rest_framework import serializers

from apps.Chat.models import Chat, Message, Participant, ChatParticipant


class StartChatSerializerInput(serializers.Serializer):
    participant_id = serializers.UUIDField()


class StartChatSerializerResponseOutput(serializers.Serializer):
    chat_id = serializers.UUIDField()
    created = serializers.BooleanField()


class BasicParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = (
            "id",
            "first_name",
            "last_name",
            "nickname",
            "avatar",
            "status",
        )


class BasicMessageSerializer(serializers.ModelSerializer):
    participant = BasicParticipantSerializer(read_only=True)

    class Meta:
        model = Message
        fields = (
            "message_type",
            "content",
            "sent_at",
            "participant",
        )


class ChatParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatParticipant
        fields = [
            "is_muted",
            "not_seen",
        ]


class ChatListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = (
            "name",
            "photo",
            "created_at",
            "last_message",
        )

    def get_last_message(self, obj):
        message = obj.messages.select_related("participant").first()

        return BasicMessageSerializer(message).data if message else None

    def get_metadata(self, obj):
        request = self.context.get("request")

        if request is None:
            return None

        chat_participant = obj.chatparticipants.filter(
            participant=request.user.participant
        ).first()

        return (
            ChatParticipantSerializer(chat_participant).data
            if chat_participant
            else None
        )


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = "__all__"
