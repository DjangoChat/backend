from apps.Chat.models import ChatParticipant
from apps.Chat.service.CreateMessageService import CreateMessageService
from apps.Chat.service.OllamaChatService import OllamaChatService
from apps.Common.models import MessageType, ParticipantType


class CreateAgentResponseService:

    def execute(self, chat, message, participant):
        agent_participant = (
            ChatParticipant.objects.filter(chat=chat)
            .filter(participant__participant_type=ParticipantType.AGENT)
            .first()
        )

        assert agent_participant is not None
        response = OllamaChatService().execute(
            chat=chat,
            prompt_type=agent_participant.participant.agent.promp_type,
            user_id=participant.user.id,
        )

        return CreateMessageService().execute(
            chat=message.chat,
            participant=agent_participant,
            message_type=MessageType.TEXT,
            content=response,
        )
