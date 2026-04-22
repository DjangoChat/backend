from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import ActivatorModel, CustomModel, RuleType, Operator

from .Policy import Policy


class Rule(CustomModel, ActivatorModel):
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name="rules",
    )
    rule_type = models.CharField(
        _("rule type"),
        max_length=20,
        choices=RuleType.choices,
    )
    attribute_name = models.CharField(
        _("attribute name"),
        max_length=100,
    )
    operator = models.CharField(
        _("operator"),
        max_length=20,
        choices=Operator.choices,
    )
    value = models.CharField(
        _("value"),
        max_length=200,
    )

    class Meta:
        db_table = "AUTHORIZATION_RULE"
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")
        indexes = [models.Index(fields=["policy"])]
        app_label = "Authorization"
