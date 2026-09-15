from apps.Chat.models import Chat, Message, Participant
from apps.Chat.service.CreateMessageService import CreateMessageService
from apps.Chat.service.OllamaChatService import OllamaChatService
from apps.Common.models import MessageType, ParticipantType


class CreateAgentResponseService:

    def execute(
        self,
        chat: Chat,
        message: Message,
        participant: Participant,
    ):
        agent_participant = Participant.objects.filter(
            chatparticipant__chat=chat,
            participant_type=ParticipantType.AGENT,
        ).first()

        assert agent_participant is not None
        response = OllamaChatService().execute(
            chat=chat,
            prompt_type=agent_participant.agent.promp_type,
            user_id=participant.user.id,
        )

        return CreateMessageService().execute(
            chat=message.chat,
            participant=agent_participant,
            message_type=MessageType.TEXT,
            content=response,
        )
