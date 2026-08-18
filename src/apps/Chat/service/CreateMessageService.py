from django.db import transaction
from django.db.models import F

from apps.Chat.models import ChatParticipant, MessageStatus, Message
from apps.Common.models import ParticipantType
from apps.Chat.tasks import create_agent_response


class CreateMessageService:

    @transaction.atomic
    def execute(
        self,
        chat,
        participant,
        message_type,
        content,
        image=None,
        attach=None,
        video=None,
    ):
        self.chat = chat
        self.participant = participant

        self._check_participant_has_permission()

        self.message = Message.objects.create(
            chat=chat,
            participant=participant,
            message_type=message_type,
            content=content,
            image=image,
            attach=attach,
            video=video,
        )

        self._update_chat_last_message()
        self._create_message_statuses()

        if participant.agent:
            transaction.on_commit(
                lambda: create_agent_response(
                    id_chat=self.chat.id,
                    id_message=self.message.id,
                    id_participant=self.participant.id,
                )
            )

        return self.message

    def _check_participant_has_permission(self):
        if not self.chat.check_participant_can_write(self.participant):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied

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
