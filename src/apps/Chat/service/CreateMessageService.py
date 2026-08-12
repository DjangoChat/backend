from django.db import transaction
from django.db.models import F

from apps.Chat.models import ChatParticipant, MessageStatus
from apps.Common.models import ParticipantType


class CreateMessageService:

    @transaction.atomic
    def execute(self, serializer, user):
        self.chat = serializer.validated_data["chat"]
        self.participant = user.participant

        self._check_participant_has_permission()
        self._create_message(serializer)
        self._update_chat_last_message()
        self._create_message_statuses()

    def _check_participant_has_permission(self):
        if not self.chat.check_participant_can_write(self.participant):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied

    def _create_message(self, serializer):
        self.message = serializer.save(participant=self.participant)

    def _update_chat_last_message(self):
        self.chat.last_message_at = self.message.sent_at
        self.chat.save(update_fields=["last_message_at"])

    def _create_message_statuses(self):
        list_participants = (
            ChatParticipant.objects.filter(self.chat)
            .exclude(self.participant)
            .exclude(participant__participant_type=ParticipantType.AGENT)
        )

        list_participants.update(
            not_seen=F("not_seen") + 1,
        )

        messages_statuses = []
        for participant in list_participants:
            messages_statuses.append(
                MessageStatus(
                    participant=participant.participant,
                    message=self.message,
                )
            )
        MessageStatus.objects.bulk_create(messages_statuses)
