from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import ActivatorModel, CustomModel
from .Policy import Policy


class Rule(CustomModel, ActivatorModel):

    RULE_TYPES = [
        ("user_attr", "User Attribute"),
        ("resource_attr", "Resource Attribute"),
        ("environment", "Environment"),
        ("relationship", "Relationship"),
    ]

    OPERATORS = [
        ("equals", "Equals"),
        ("not_equals", "Not Equals"),
        ("contains", "Contains"),
        ("in", "In"),
        ("gt", "Greater Than"),
        ("lt", "Less Than"),
        ("gte", "Greater Than or Equal"),
        ("lte", "Less Than or Equal"),
    ]

    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        related_name="rules",
    )
    rule_type = models.CharField(
        _("rule type"),
        max_length=20,
        choices=RULE_TYPES,
    )
    attribute_name = models.CharField(
        _("attribute name"),
        max_length=100,
    )
    operator = models.CharField(
        _("operator"),
        max_length=20,
        choices=OPERATORS,
    )
    value = models.CharField(
        _("value"),
        max_length=200,
    )
    effect = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "AUTHORIZATION_RULE"
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")
        indexes = [models.Index(fields=["policy"])]
        app_label = "Authorization"
