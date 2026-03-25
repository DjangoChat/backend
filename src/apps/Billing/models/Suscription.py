from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, StatusSuscription


class Suscription(CustomModel):
    strip_sucription_id = models.CharField(
        _("Stripe suscription id"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        _("Start date"),
        auto_now_add=True,
    )
    end_date = models.DateField(
        _("Final date"),
        null=True,
        blank=True,
    )
    current_period_start = models.DateTimeField(
        _("Start date of the current period"),
    )
    current_period_end = models.DateTimeField(
        _("End date of the current period"),
    )
    status = models.CharField(
        _("Status of the suscription"),
        max_length=100,
        choices=StatusSuscription,
    )

    # Snapshot of price table
    amount = models.PositiveBigIntegerField(
        _("Amount on cents"),
    )
    currency_code = models.CharField(
        max_length=3,
    )
    plan_name = models.CharField(
        _("Plan name"),
        max_length=100,
    )
    plan_interval_unit = models.CharField(
        _("The name of the period"),
        max_length=100,
    )

    class Meta:
        db_table = "BILLING_SUSCRIPTION"
        verbose_name = _("Suscription")
        verbose_name_plural = _("Suscriptions")
        app_label = "Billing"
