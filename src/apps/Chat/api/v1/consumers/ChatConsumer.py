import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError

from apps.Chat.api.v1.serializers import (
    BaseEventSerializer,
    DeleteMessageSerializer,
    MessageDetailedSerializer,
    ReactMessageSerializer,
    SeenSerializer,
    SendMessageSerializer,
    TypingSerializer,
)
from apps.Chat.models import Chat, Message
from apps.Common.models import ConsumerCommand, MessageType

EVENT_SERIALIZERS = {
    "send_message": SendMessageSerializer,
    "typing": TypingSerializer,
    "seen": SeenSerializer,
    "delete_message": DeleteMessageSerializer,
    "react_message": ReactMessageSerializer,
}


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]  # type: ignore
        chat_id = self.scope["url_route"]["kwargs"]["conversation_id"]  # type: ignore
        chat = self.get_chat(chat_id)

        if chat is None:
            raise NotFound

        self.chat = chat
        self.chat_room_socket__name = f"chat_room__{self.chat.id}"  # type: ignore

        if not self.check_user_has_perm():
            raise PermissionDenied

        async_to_sync(self.channel_layer.group_add)(
            self.chat_room_socket__name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room_socket__name,
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
        if event_type == ConsumerCommand.CREATE_MESSAGE:
            return

        if event_type == ConsumerCommand.DELETE_MESSAGE:
            return

        if event_type == ConsumerCommand.UPDATE_MESSAGE:
            return

        raise ValidationError("There is no event type that match this request")

    def get_chat(self, chat_id):
        return Chat.objects.filter(id=chat_id).first()

    def check_user_has_perm(self):
        return Chat.objects.filter(
            id=self.chat.id,
            chatparticipant__participant__user=self.user,
        ).exists()
