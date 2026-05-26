from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, AgentName, AgentType
from .Nature import Nature


class Agent(CustomModel):
    name = models.CharField(
        _("Name of the agent"),
        choices=AgentName,
        max_length=50,
    )
    description = models.CharField(
        _("Descripcion of the agent"),
    )
    promp_type = models.TextField(
        _("Description of the agent conduct"),
    )
    avatar = models.ImageField(
        upload_to="avatar_images/",
        blank=True,
        null=True,
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
