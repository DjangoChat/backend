from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import ActivatorModel, CustomModel


class Policy(CustomModel, ActivatorModel):

    name = models.CharField(
        _("name"),
        max_length=200,
    )
    description = models.CharField(
        _("description"),
        blank=True,
    )
    resource_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    # view, edit, delete, add
    action = models.CharField(
        _("action"),
        max_length=50,
    )
    # higher priority wins
    priority = models.IntegerField(
        _("priority"),
        default=0,
    )

    class Meta:
        db_table = "AUTHORIZATION_POLICY"
        verbose_name = _("Policy")
        verbose_name_plural = _("Policies")
        indexes = [models.Index(fields=["resource_type"])]
        ordering = ["-priority", "id"]
        app_label = "Authorization"
