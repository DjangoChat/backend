from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, ParticipantStatus, ParticipantType

from .Agent import Agent


class Participant(CustomModel):
    participant_type = models.CharField(
        _("Type of entity which is talking"),
        max_length=20,
        choices=ParticipantType,
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    agent = models.OneToOneField(
        Agent,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    nickname = models.CharField(
        _("Nickname"),
        max_length=150,
    )
    avatar = models.ImageField(
        upload_to="participant_avatar/",
        blank=True,
        null=True,
    )
    participant_status = models.CharField(
        _("Status of the participant"),
        choices=ParticipantStatus,
        default=ParticipantStatus.EN_LINEA,
    )

    class Meta:
        db_table = "CHAT_PARTICIPANT"
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        app_label = "Chat"
        constraints = [
            models.CheckConstraint(
                name="participant_user_xor_agent",
                condition=(
                    (Q(user__isnull=False) & Q(agent__isnull=True))
                    | (Q(user__isnull=True) & Q(agent__isnull=False))
                ),
            )
        ]

    def clean(self) -> None:
        super().clean()

        if self.user == None and self.agent == None:
            raise ValidationError(
                "Both fields user and agent can not be empty at the same time."
            )

        if self.user != None and self.agent != None:
            raise ValidationError(
                "Both fields user and agent can not be fullfill at the same time."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
