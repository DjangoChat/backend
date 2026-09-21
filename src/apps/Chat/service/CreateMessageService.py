from django.db import transaction
from django.db.models import F

from apps.Chat.models import Chat, ChatParticipant, Message, MessageStatus, Participant
from apps.Common.models import ParticipantType


class CreateMessageService:

    @transaction.atomic
    def execute(
        self,
        chat: Chat,
        participant: Participant,
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

        # Trigger agent response only if:
        # 1. Chat has an agent participant AND
        # 2. The sender is a user (not the agent itself)
        agent_in_chat = ChatParticipant.objects.filter(
            chat=self.chat,
            participant__participant_type=ParticipantType.AGENT,
        ).exists()

        if agent_in_chat and self.participant.participant_type == ParticipantType.USER:

            def trigger_agent():
                from apps.Chat.tasks import create_agent_response

                create_agent_response.delay(
                    id_chat=self.chat.id,
                    id_message=self.message.id,
                    id_participant=self.participant.id,
                )  # type: ignore

            transaction.on_commit(trigger_agent)

        return self.message

    def _check_participant_has_permission(self):
        if self.participant.agent:
            return

        if not self.chat.check_participant_can_write(self.participant):
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied

    def _update_chat_last_message(self):
        self.chat.last_message_at = self.message.sent_at
        self.chat.save(update_fields=["last_message_at"])

    def _create_message_statuses(self):
        list_participants = (
            ChatParticipant.objects.filter(chat=self.chat)
            .exclude(id=self.participant.id)
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
