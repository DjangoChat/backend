from django.db import models
from django.utils.translation import gettext_lazy as _


class PlanOption(models.TextChoices):
    FREE = "FREE", _("Free")
    PRO = "PRO", _("Pro")
    PREMIUM = "PREMIUM", _("Premium")
