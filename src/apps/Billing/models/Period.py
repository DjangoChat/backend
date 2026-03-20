from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, Frequency


class Period(CustomModel):
    name = models.CharField(
        _("The frequency"),
        max_length=100,
        choices=Frequency,
    )
    interval_count = models.PositiveIntegerField(
        _("Number of months"),
    )
    interval_unit = models.CharField(
        _("The name of the period"),
        max_length=100,
    )

    class Meta:
        db_table = "BILLING_PERIOD"
        verbose_name = _("Period")
        verbose_name_plural = _("Periods")
