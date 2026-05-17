from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel


class Chat(CustomModel):
    last_message = models.TextField(
        _("Last message send"),
    )
    created_at = models.DateTimeField(
        _("The time the chat was created"),
        auto_now_add=True,
    )
    id_conversation_chatpgt = models.CharField(
        _("Id of the conversation created for chatgpt")
    )

    class Meta:
        db_table = "CHAT_CHAT"
        verbose_name = _("Chat")
        verbose_name_plural = _("Chats")
        app_label = "Chat"
