from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from apps.Common.models import CustomModel, ParticipantType
from .Agent import Agent

from django.core.exceptions import ValidationError


class Participant(CustomModel):
    participaty_type = models.CharField(
        _("Type of entity which is talking"),
        max_length=20,
        choices=ParticipantType,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
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
