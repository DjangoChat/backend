from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusSuscription(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    CANCELED = "CANCELED", _("Canceled")
