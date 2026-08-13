from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from apps.Chat.models import Message

from .BaseOllamaService import BaseOllamaService


class OllamaChatService(BaseOllamaService):
    def execute(self, chat, prompt_type, user_id):
        last_messages = Message.objects.filter(chat=chat).values_list(
            "content",
            "participant__participant_type",
        )[:20]

        messages = [
            SystemMessage(content=prompt_type)
            + [
                (
                    HumanMessage(content)
                    if type_user == "user"
                    else AIMessage(content=content)
                )
                for content, type_user in last_messages
            ]
        ]

        return self.ollama_repo.chat(messages=messages, user_id=user_id)
