from django.db import models
from django.utils.translation import gettext_lazy as _


class PlanOption(models.TextChoices):
    MEMBER = "MEMBER", _("Member")
    PRO = "PRO", _("Pro")
    PREMIUM = "PREMIUM", _("Premium")
