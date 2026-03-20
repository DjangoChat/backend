from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel
from .Plan import Plan


class Quota(CustomModel):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        _("Code of limiter"),
        max_length=100,
    )
    limit = models.PositiveIntegerField(
        _("Limit of quota"),
    )

    class Meta:
        db_table = "BILLING_QUOTA"
        verbose_name = _("Quota")
        verbose_name_plural = _("Quotas")
