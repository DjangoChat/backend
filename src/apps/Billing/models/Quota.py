from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, QuotaCode


class Quota(CustomModel):
    code = models.CharField(
        _("Code of limiter"),
        unique=True,
        max_length=100,
        choices=QuotaCode,
    )
    name = models.CharField(
        _("Name of the feature"),
        max_length=50,
    )
    description = models.CharField(
        _("Description of the feature"),
        max_length=100,
    )

    class Meta:
        db_table = "BILLING_QUOTA"
        verbose_name = _("Quota")
        verbose_name_plural = _("Quotas")
        app_label = "Billing"
