from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.Common.models import ActivatorModel, CustomModel

from .Policy import Policy


class RuleType(models.TextChoices):
    USER_ATTR = "user_attr", _("User Attribute")
    RESOURCE_ATTR = "resource_attr", _("Resource Attribute")
    ENVIRONMENT = "environment", _("Environment")
    RELATIONSHIP = "relationship", _("Relationship")
    AMOUNT = "amount", _("Quantity")


class Operator(models.TextChoices):
    EQUALS = "equals", _("Equals")
    NOT_EQUALS = "not_equals", _("Not Equals")
    CONTAINS = "contains", _("Contains")
    IN = "in", _("In")
    GREATER_THAN = "gt", _("Greater Than")
    LESS_THAN = "lt", _("Less Than")
    GREATER_THAN_OR_EQUAL = "gte", _("Greater Than or Equal")
    LESS_THAN_OR_EQUAL = "lte", _("Less Than or Equal")


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
    effect = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "AUTHORIZATION_RULE"
        verbose_name = _("Rule")
        verbose_name_plural = _("Rules")
        indexes = [models.Index(fields=["policy"])]
        app_label = "Authorization"
