from django.db import models
from django.utils.translation import gettext_lazy as _


class Period(models.TextChoices):
    MONTHLY = "MONTHLY", _("Monthly")
    TRIMESTER = "TRIMESTER", _("Trimester")
    ANNUAL = "ANNUAL", _("Annual")
