from apps.Chat.service import OllamaChatService, CreateMessageService
from apps.Chat.models import ChatParticipant, Message
from apps.Common.models import MessageType, ParticipantType


class CreateAgentResponseService:

    def execute(self, chat, message, participant):
        response = OllamaChatService().execute(
            chat=chat,
            prompt_type=participant.agent.promp_type,
        )

        agent_participant = (
            ChatParticipant.objects.filter(chat=chat)
            .filter(participant__participant_type=ParticipantType.AGENT)
            .first()
        )

        return CreateMessageService().execute(
            chat=message.chat,
            participant=agent_participant,
            message_type=MessageType.TEXT,
            content=response,
        )
