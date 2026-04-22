from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusSuscription(models.TextChoices):
    ACTIVE = "ACTIVE", _("Active")
    CANCELED = "CANCELED", _("Canceled")


class PlanOption(models.TextChoices):
    MEMBER = "MEMBER", _("Member")
    PRO = "PRO", _("Pro")
    PREMIUM = "PREMIUM", _("Premium")


class Gender(models.TextChoices):
    FEMALE = "FEMALE", _("Female")
    MALE = "MALE", _("Male")
    CUSTOM = "CUSTOM", _("Custom")
    NONE = "NONE", _("Prefer not to say")


class Frequency(models.TextChoices):
    MONTHLY = "MONTHLY", _("Monthly")
    TRIMESTER = "TRIMESTER", _("Trimester")
    ANNUAL = "ANNUAL", _("Annual")


class EndpointOption(models.TextChoices):
    VIEW = "VIEW", _("view")
    EDIT = "EDIT", _("edit")
    DELETE = "DELETE", _("delete")


class CustomGroups(models.TextChoices):
    MEMBER = "MEMBER", ("Member")
    MAINTAINER = "MAINTAINER", ("Maintainer")
    ANALITICAL = "ANALITICAL", ("Analitical")
    ADMIN = "ADMIN", ("Admin")


class RuleType(models.TextChoices):
    USER_ATTR = "user_attr", _("User Attribute")
    RESOURCE_ATTR = "resource_attr", _("Resource Attribute")
    ENVIRONMENT = "environment", _("Environment")
    RELATIONSHIP = "relationship", _("Relationship")


class Operator(models.TextChoices):
    EQUALS = "equals", _("Equals")
    NOT_EQUALS = "not_equals", _("Not Equals")
    CONTAINS = "contains", _("Contains")
    IN = "in", _("In")
    GREATER_THAN = "gt", _("Greater Than")
    LESS_THAN = "lt", _("Less Than")
    GREATER_THAN_OR_EQUAL = "gte", _("Greater Than or Equal")
    LESS_THAN_OR_EQUAL = "lte", _("Less Than or Equal")
