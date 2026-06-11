from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, MessageStatusType
from apps.Chat.models import Participant, Message


class MessageStatus(CustomModel):
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        _("Status of the message"),
        max_length=20,
        choices=MessageStatusType,
        default=MessageStatusType.DELIVER,
    )
    upload_at = models.DateTimeField(
        _("Last update"),
        auto_now_add=True,
    )

    class Meta:
        db_table = "CHAT_MESSAGE_STATUS"
        verbose_name = _("Message Status")
        verbose_name_plural = _("Message Statuses")
        app_label = "Chat"
