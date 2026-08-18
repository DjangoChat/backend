from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, PlanOption

from .Currency import Currency
from .Period import Period
from .Plan import Plan


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
    stripe_price_id = models.CharField(
        _("Stripe price"),
        null=True,
        unique=True,
    )

    class Meta:
        db_table = "BILLING_PRICE"
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")
        app_label = "Billing"
