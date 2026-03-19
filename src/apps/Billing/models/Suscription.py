from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel
from .Plan import Plan


class Suscription(CustomModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
    )
    start_date = models.DateTimeField(
        _("Start date"),
        auto_now_add=True,
    )

    class Meta:
        db_table = "BILLING_SUSCRIPTION"
        verbose_name = _("Suscription")
        verbose_name_plural = _("Suscriptions")
