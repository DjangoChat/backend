from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, Period, PlanOption


class Plan(CustomModel):
    name = models.CharField(
        _("Plan name"),
        max_length=100,
        choices=PlanOption,
    )
    frequency = models.CharField(
        _("Frequency"),
        max_length=50,
        choices=Period,
    )
    real_amount = models.PositiveIntegerField(
        _("Whole numbers"),
    )
    real_cent = models.PositiveIntegerField(
        _("Cents"),
    )
    discount_amount = models.PositiveIntegerField(
        _("Whole numbers discount"),
        blank=True,
        null=True,
    )
    discount_cent = models.PositiveIntegerField(
        _("Cents discount"),
        blank=True,
        null=True,
    )
    description = models.TextField(
        _("Description"),
        max_length=500,
    )

    class Meta:
        db_table = "BILLING_PLAN"
        unique_together = [["name", "frequency"]]
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
