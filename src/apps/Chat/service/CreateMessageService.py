from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from apps.Chat.api.v1.serializers import (
    ChatDetailedSerializer,
    MessageDetailedSerializer,
)
from apps.Chat.models import ChatParticipant, MessageStatus, Chat


class CreateMessageService:

    @transaction.atomic
    def execute(self, serializer, user):
        self.chat = get_object_or_404(Chat, serializer.data["id"])
        self.participant = user.participant

        self._check_participant_has_permission()
        self._create_message(serializer)
        self._create_message_statuses_update_not_seen()
        self._update_chat_last_message()
        self._send_event_notification_consumer(user)
        self._send_even_chat_consumer()

    def _create_message(self, serializer):
        self.message = serializer.save(participant=self.participant)

    def _create_message_statuses_update_not_seen(self):
        chat_participants = ChatParticipant.objects.filter(
            chat=self.chat,
        ).exclude(
            participant=self.participant,
        )
        chat_participants.update(
            not_seen=F("not_seen") + 1,
        )
        messages_statuses = []
        for chat_participant in chat_participants:
            messages_statuses.append(
                MessageStatus(
                    participant=chat_participant.participant,
                    message=self.message,
                )
            )
        MessageStatus.objects.bulk_create(*messages_statuses)

    def _check_participant_has_permission(self):
        if not self.chat.check_participant_can_write(self.participant):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied

    def _update_chat_last_message(self):
        self.chat.last_message_at(self.message.sent_at).save()

    def _send_event_notification_consumer(self, user):
        channel_layer = get_channel_layer()

        chat_participants = ChatParticipant.objects.filter(
            chat=self.chat,
        ).exclude(
            participant=self.participant,
        )
        for chatparticipant in chat_participants:
            user = chatparticipant.participant.user
            channel_name = f"notification__{user.id}"

            async_to_sync(channel_layer.group_send)(  # type: ignore
                channel_name,
                {
                    "type": "chat_message",
                    "data": ChatDetailedSerializer(self.chat).data,
                },
            )

    # TODO: improve the overall logic of this file
    # TODO: change the name of the type on both functions
    def _send_even_chat_consumer(self):
        channel_layer = get_channel_layer()
        channel_name = f"chat_room__{self.chat.id}"

        async_to_sync(channel_layer.group_send)(  # type: ignore
            channel_name,
            {
                "type": "chat_message",
                "data": MessageDetailedSerializer(self.message).data,
            },
        )
