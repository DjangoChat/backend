import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.Chat.models import Chat, Message
from apps.Chat.api.v1.serializers import MessageSerializer
from apps.Common.models import MessageType, ConversationConsumerType
from apps.Chat.api.v1.serializers import (
    SendMessageSerializer,
    TypingSerializer,
    SeenSerializer,
    DeleteMessageSerializer,
    ReactMessageSerializer,
    BaseEventSerializer,
)

EVENT_SERIALIZERS = {
    "send_message": SendMessageSerializer,
    "typing": TypingSerializer,
    "seen": SeenSerializer,
    "delete_message": DeleteMessageSerializer,
    "react_message": ReactMessageSerializer,
}


class ConversationConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]  # type: ignore
        chat_id = self.scope["url_route"]["kwargs"]["conversation_id"]  # type: ignore

        chat = self.get_chat(chat_id)

        if chat is None:
            raise NotFound

        self.chat = chat
        self.group_name = f"conversation_chat_id{self.chat.id}"  # type: ignore

        if not self.check_user_has_perm():
            raise PermissionDenied

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        base_serializer = BaseEventSerializer(data=data)
        base_serializer.is_valid(raise_exception=True)

        event_type = base_serializer.validated_data["type"]  # type: ignore

        serializer_class = EVENT_SERIALIZERS[event_type]
        serializer = serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        # TODO: create service for all this endpoints
        # TODO: check if can receive multipartparses for images,files,videos
        if event_type == ConversationConsumerType.CREATE_MESSAGE:
            new_message = Message.objects.create(
                chat=self.chat,
                participant=self.user.participant,  # type: ignore
                message_type=MessageType.TEXT,
                content=validated_data["content"],
            )
            self.send(
                text_data=json.dumps(
                    {
                        "type": "add_message",
                        "messages": MessageSerializer(new_message),
                    }
                )
            )

        if event_type == ConversationConsumerType.DELETE_MESSAGE:
            return

        if event_type == ConversationConsumerType.UPDATE_MESSAGE:
            return
        if event_type == ConversationConsumerType.PATH_MESSAGE_STATUS_STATUS:
            return

        if event_type == ConversationConsumerType.PATCH_CHAT_PARTICIPANT_IS_TYPING:
            return

        raise ValidationError("There is no event type that match this request")

    def get_chat(self, chat_id):
        return Chat.objects.filter(id=chat_id).first()

    def check_user_has_perm(self):
        return Chat.objects.filter(
            id=self.chat.id,
            chatparticipant__participant__user=self.user,
        ).exists()
