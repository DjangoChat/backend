from rest_framework import serializers

from apps.Chat.models import Chat, ChatParticipant, Message, Participant


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
            "participant_status",
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


class ChatDetailedSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    metadata = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "name",
            "photo",
            "last_message",
            "metadata",
            "participants",
        ]

    def get_last_message(self, obj):
        message = obj.message_set.select_related("participant").first()

        return BasicMessageSerializer(message).data if message else None

    def get_metadata(self, obj):
        request = self.context.get("request")

        if request is None:
            return None

        chat_participant = obj.chatparticipant_set.filter(
            participant=request.user.participant
        ).first()

        return (
            ChatParticipantSerializer(chat_participant).data
            if chat_participant
            else None
        )

    def get_participants(self, obj):
        request = self.context.get("request")

        if request is None:
            return None

        participant = request.user.participant
        return (
            Participant.objects.filter(chatparticipant__chat=obj)
            .exclude(id=participant.id)
            .values_list("id", flat=True)
        )


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = "__all__"
