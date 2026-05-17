from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel
from apps.Chat.models import Chat, Participant


class ChatParticipant(CustomModel):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )
    joined_at = models.DateTimeField(
        _("Time the user/agent join the conversation"),
        auto_now_add=True,
    )
    is_muted = models.BooleanField(
        _("Check if the user muted the chat"),
        default=False,
    )

    class Meta:
        db_table = "CHAT_CHAT_PARTICIPANT"
        verbose_name = _("Chat Participant")
        verbose_name_plural = _("Chat Participants")
        unique_together = ("chat", "participant")
        app_label = "Chat"
