from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from commons.models import CustomModel, ActivatorModel


class UserProfile(CustomModel, ActivatorModel):
    class Gender(models.TextChoices):
        FEMALE = "FEMALE", _("Female")
        MALE = "MALE", _("Male")
        CUSTOM = "CUSTOM", _("Custom")
        NONE = "NONE", _("Prefer not to say")

    class Clearance(models.TextChoices):
        LOW = "LOW", _("Low")
        MEDIUM = "MEDIUM", _("Medium")
        HIGH = "HIGH", _("High")

    class Role(models.TextChoices):
        BASIC = "BASIC", _("Basic")
        CONTROL = "CONTROL", _("Control")
        ANALYTIC = "ANALYTIC", _("Analytic")
        ADMIN = "ADMIN", _("Admin")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(
        _("first name"),
        max_length=150,
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
    )
    gender = models.CharField(
        _("gender"),
        max_length=20,
        choices=Gender.choices,
    )
    custom_gender = models.CharField(
        _("custom gender"),
        max_length=255,
        blank=True,
        null=True,
    )
    birth_date = models.DateTimeField(
        _("birth date"),
    )
    department = models.CharField(
        _("department"),
        max_length=100,
        blank=True,
        null=True,
    )
    clearance_level = models.CharField(
        _("clearance level"),
        max_length=20,
        choices=Clearance.choices,
    )
    role = models.CharField(
        _("role"),
        max_length=20,
        choices=Role.choices,
        default=Role.BASIC,
    )
