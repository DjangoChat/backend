from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

from apps.Common.models import ActivatorModel, CustomModel, ActivatorModelManager


class CustomUserManager(BaseUserManager, ActivatorModelManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(CustomModel, AbstractBaseUser, ActivatorModel):
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    phone = PhoneNumberField(
        unique=True,
    )
    verified = models.BooleanField(
        _("verified"),
        default=True,
        help_text=_("Designates whether this user has activated its account or not. "),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        app_label = "Authentication"
