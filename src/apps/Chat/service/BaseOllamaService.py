from django.conf import settings

from apps.Chat.repository import OllamaRepository


class BaseOllamaService:

    def __init__(self):
        self.ollama_repo = OllamaRepository(
            settings.OLLAMA_MODEL,
            settings.OLLAMA_URL,
        )
