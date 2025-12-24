from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class ActivatorModel(models.Model):
    INACTIVE_STATUS = 0
    ACTIVE_STATUS = 1

    STATUS_CHOICES = (
        (INACTIVE_STATUS, _("Inactive")),
        (ACTIVE_STATUS, _("Active")),
    )

    status = models.IntegerField(
        _("status"),
        choices=STATUS_CHOICES,
        default=ACTIVE_STATUS,
    )
    activate_date = models.DateField(
        blank=True,
        null=True,
        help_text=_("keep empty for an immediative activation"),
    )
    deactivate_date = models.DateField(
        blank=True,
        null=True,
        help_text=_("keep empty for indefinite activation"),
    )

    class Meta:
        ordering = (
            "status",
            "-activate_date",
        )
        abstract = True

    def save(self, *args, **kwargs):
        if not self.activate_date:
            self.activate_date = now()
        super().save(*args, **kwargs)
