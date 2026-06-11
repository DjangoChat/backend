from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, AgentType
from .Nature import Nature


class Agent(CustomModel):
    promp_type = models.TextField(
        _("Description of the agent conduct"),
    )
    natures = models.ManyToManyField(
        Nature,
    )
    agent_type = models.CharField(
        _("Type of agent"),
        max_length=20,
        choices=AgentType,
    )

    class Meta:
        db_table = "AUTHENTICATION_AGENT"
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")
        app_label = "Chat"
        indexes = [
            models.Index(fields=["agent_type"]),
        ]
