from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, MessageType
from apps.Chat.models import Chat, Participant
from apps.Common.models import MessageStatusType

from django.core.exceptions import ValidationError


class Message(CustomModel):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
    )
    participant = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
    )
    message_type = models.CharField(
        _("Message type"),
        max_length=20,
        choices=MessageType,
    )
    content = models.TextField(
        _("Content of the message"),
        null=True,
        blank=True,
    )
    image = models.ImageField(
        _("Image attached"),
        null=True,
        blank=True,
    )
    attach = models.FileField(
        _("File attached"),
        null=True,
        blank=True,
    )
    video = models.FileField(
        _("Video attached"),
        null=True,
        blank=True,
    )
    sent_at = models.DateTimeField(
        _("Time the message was created"),
        auto_now_add=True,
    )

    class Meta:
        db_table = "CHAT_MESSAGE"
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        app_label = "Chat"
        ordering = ["-sent_at"]
        indexes = [
            models.Index(fields=["message_type"]),
        ]

    def clean(self) -> None:
        super().clean()

        if (
            self.message_type == MessageType.FILE
            or self.message_type == MessageType.VIDEO
        ) and self.content != None:
            raise ValidationError("No es posible adjuntar mensajes a archivos o videos")

        if self.message_type == MessageType.TEXT and self.content == None:
            raise ValidationError("The message can not be empty")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def has_been_seen_by_all(self) -> bool:
        return not self.messagestatus_set.exclude(  # type: ignore
            status=MessageStatusType.READ
        ).exists()
