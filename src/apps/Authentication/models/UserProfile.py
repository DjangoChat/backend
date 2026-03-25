from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import ActivatorModelManager, CustomModel, Gender


class UserProfile(CustomModel):
    objects: ActivatorModelManager = ActivatorModelManager()
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    nickname = models.CharField(
        _("Nickname"),
        max_length=150,
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
    avatar = models.ImageField(
        upload_to="avatar_images/",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "AUTHENTICATION_PROFILE"
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        indexes = [models.Index(fields=["user"])]
        app_label = "Authentication"
