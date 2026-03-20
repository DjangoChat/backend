from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, PlanOption
from .Plan import Plan
from .Period import Period
from .Currency import Currency


class Price(CustomModel):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
    )
    period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveBigIntegerField(
        _("Amount on cents"),
    )

    class Meta:
        db_table = "BILLING_PRICE"
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")
