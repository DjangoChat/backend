from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, NatureType


class Nature(CustomModel):
    name = models.CharField(
        _("Name of the nature"),
        max_length=50,
        choices=NatureType,
    )
    description = models.CharField(
        _("Description of the nature"),
    )

    class Meta:
        db_table = "CHAT_NATURE"
        verbose_name = _("Nature")
        verbose_name_plural = _("Nature")
        app_label = "Chat"
