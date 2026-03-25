from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.TextChoices):
    FEMALE = "FEMALE", _("Female")
    MALE = "MALE", _("Male")
    CUSTOM = "CUSTOM", _("Custom")
    NONE = "NONE", _("Prefer not to say")
