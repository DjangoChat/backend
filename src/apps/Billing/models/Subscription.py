from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Billing.models import Price
from apps.Common.models import CustomModel, StatusSuscription


class Subscription(CustomModel):
    stripe_subscription_id = models.CharField(
        _("Stripe suscription id"),
        null=True,
        unique=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        _("Start date"),
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
    period_name = models.CharField(
        _("Period name"),
        max_length=100,
    )

    class Meta:
        db_table = "BILLING_SUBSCRIPTION"
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        ordering = ["start_date"]
        app_label = "Billing"

    def has_feature(self):
        return None

    def get_quota_limit(self):
        return None

    def get_quota_usage(self):
        return None

    def get_quota_remaining(self):
        return None

    def can_consume(self):
        return None

    def consume(self):
        return None
