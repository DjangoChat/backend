from .BaseOllamaService import BaseOllamaService

from apps.Chat.models import Message
from apps.Common.models import ParticipantType


class OllamaChatService(BaseOllamaService):
    def execute(self, chat, prompt_type=""):
        last_messages = Message.objects.filter(chat=chat).values_list(
            "content",
            "participant__participant_type",
        )[:50]
        return self.ollama_repo.chat(
            messages=[{"role": "system", "content": prompt_type}]
            + [
                {
                    "role": ("assistant" if j == ParticipantType.AGENT else "user"),
                    "content": i,
                }
                for i, j in last_messages
            ],
        )["message"]["content"]
