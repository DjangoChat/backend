from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from apps.Chat.models import Message
from apps.Common.models import ParticipantType

from .BaseOllamaService import BaseOllamaService


class OllamaChatService(BaseOllamaService):
    def execute(self, chat, prompt_type, user_id):
        last_messages = list(
            Message.objects.filter(chat=chat).order_by("-sent_at").values_list(
                "content",
                "participant__participant_type",
            )[:10]
        )[::-1]

        messages = [
            SystemMessage(content=prompt_type),
            *[
                (
                    HumanMessage(content=content)
                    if type_user == ParticipantType.USER
                    else AIMessage(content=content)
                )
                for content, type_user in last_messages
            ],
        ]

        return self.ollama_repo.chat(messages=messages, user_id=user_id)
