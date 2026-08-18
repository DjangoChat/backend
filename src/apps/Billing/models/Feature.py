from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import CustomModel, FeatureCode


class Feature(CustomModel):
    code = models.CharField(
        _("Code to identify the feature"),
        unique=True,
        choices=FeatureCode,
    )
    name = models.CharField(
        _("Name of the feature"),
        max_length=50,
    )
    description = models.CharField(
        _("Description of the feature"),
        max_length=100,
    )

    class Meta:
        db_table = "BILLING_FEATURE"
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")
        app_label = "Billing"
