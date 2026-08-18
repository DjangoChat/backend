from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import AgentType, CustomModel

from .Nature import Nature


class Agent(CustomModel):
    promp_type = models.TextField(
        _("Prompt that will be attach to the conversation"),
    )
    natures = models.ManyToManyField(
        Nature,
    )
    description = models.TextField(
        _("Description of the agent"),
    )
    agent_type = models.CharField(
        _("Type of agent"),
        max_length=20,
        choices=AgentType,
    )

    class Meta:
        db_table = "CHAT_AGENT"
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")
        app_label = "Chat"
        indexes = [
            models.Index(fields=["agent_type"]),
        ]
