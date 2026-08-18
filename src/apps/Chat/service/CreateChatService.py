from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied

from apps.Chat.models import Chat, ChatParticipant, Participant
from apps.Common.models import AgentType, FeatureCode

PERMISSION = {
    AgentType.BASIC: FeatureCode.BASIC_AGENT,
    AgentType.MEDIUM: FeatureCode.MEDIUM_AGENT,
    AgentType.ADVANCE: FeatureCode.ADVANCED_AGENT,
}


class CreateChatService:

    @transaction.atomic
    def execute(self, current_user, other_participant_id):
        other_participant = get_object_or_404(Participant, id=other_participant_id)
        exits_chat = self._check_exist_chat(current_user, other_participant)

        if exits_chat:
            return exits_chat, False

        self._check_have_permission(current_user, other_participant)
        chat = self._create_chat_assing_participants(current_user, other_participant)
        return chat, True

    def _check_exist_chat(self, current_participant, other_participant):
        return (
            Chat.objects.all_user_chats(current_participant)
            .filter(
                chatparticipant__participant=other_participant,
            )
            .first()
        )

    def _create_chat_assing_participants(self, current_user, other_participant):
        chat = Chat.objects.create()
        ChatParticipant.objects.bulk_create(
            [
                ChatParticipant(
                    chat=chat,
                    participant=current_user.participant,
                ),
                ChatParticipant(
                    chat=chat,
                    participant=other_participant,
                ),
            ]
        )
        return chat

    def _check_have_permission(self, current_participant, other_participant):
        if (
            other_participant.agent
            and not current_participant.get_last_valid_subscription().has_feature(
                PERMISSION[other_participant.agent.agent_type]
            )
        ):
            raise PermissionDenied

        # TODO: add validation when model matching is made
        if other_participant.user:
            pass
