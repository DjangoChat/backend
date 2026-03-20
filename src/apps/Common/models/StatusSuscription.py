from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusSuscription(models.TextChoices):
    SELECTED = "SELECTED", _("Selected")
    CANCELED = "CANCELED", _("Canceled")
