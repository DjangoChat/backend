from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel


class Agent(CustomModel):
    name = models.CharField(
        _("Name of the agent"),
    )
    promp_type = models.TextField(
        _("Description of the agent conduct"),
    )
    avatar = models.ImageField(
        upload_to="avatar_images/",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "AUTHENTICATION_AGENT"
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")
        app_label = "Authentication"
