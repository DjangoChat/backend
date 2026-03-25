from django.db import models
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    code = models.CharField(
        primary_key=True,
        max_length=3,
    )
    name = models.CharField(
        _("Name of the currency"),
        max_length=100,
    )
    simbol = models.CharField(
        _("Simbol"),
        max_length=20,
    )

    class Meta:
        db_table = "BILLING_CURRENCY"
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")
        app_label = "Billing"
