from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel

from .Quota import Quota
from .Subscription import Subscription


class Usage(CustomModel):
    quota = models.ForeignKey(
        Quota,
        on_delete=models.CASCADE,
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
    )
    count = models.PositiveIntegerField(
        _("Number of time apply"),
    )

    class Meta:
        db_table = "BILLING_USAGE"
        unique_together = [["quota", "subscription"]]
        verbose_name = _("Usage")
        verbose_name_plural = _("Usages")
        app_label = "Billing"
