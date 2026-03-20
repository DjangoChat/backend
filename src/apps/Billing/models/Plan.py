from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, PlanOption


class Plan(CustomModel):
    name = models.CharField(
        _("Plan name"),
        max_length=100,
        choices=PlanOption,
    )
    description = models.TextField(
        _("Description"),
        max_length=500,
    )
    stripe_product_id = models.CharField(
        _("Stripe product"),
    )

    class Meta:
        db_table = "BILLING_PLAN"
        unique_together = [["name", "frequency"]]
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
