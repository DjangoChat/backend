from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel

from .Plan import Plan
from .Quota import Quota


class QuotaPlan(CustomModel):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
    )
    quota = models.ForeignKey(
        Quota,
        on_delete=models.CASCADE,
    )
    limit = models.PositiveBigIntegerField(
        null=True,
    )

    class Meta:
        db_table = "BILLING_QUOTA_PLAN"
        verbose_name = _("Quota Plan")
        verbose_name_plural = _("Quotas Plans")
        app_label = "Billing"
