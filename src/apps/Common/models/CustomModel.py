import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from .ActivatorModel import ActivatorModel

class CustomModel(ActivatorModel):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    class Meta:
        app_label = "Common"
        abstract = True
