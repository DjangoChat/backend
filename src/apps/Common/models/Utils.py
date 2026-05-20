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


class ParticipantType(models.TextChoices):
    USER = "USER", _("User")
    AGENT = "AGENT", _("AGENT")


class MessageType(models.TextChoices):
    TEXT = "TEXT", _("Text")
    VIDEO = "VIDEO", _("Video")
    FILE = "FILE", _("File")
    IMAGE = "IMAGE", _("Image")


class MessageStatusType(models.TextChoices):
    NOT_DELIVER = "NOT_DELIVER", _("Not yet deliver")
    DELIVER = "DELIVER", _("Delivar")
    READ = "READ", _("Read")


class NatureType(models.TextChoices):
    ANALYTICAL = "analytical", _("Analytical")
    CREATIVE = "creative", _("Creative")
    EMPATHETIC = "empathetic", _("Empathetic")
    LOGICAL = "logical", _("Logical")
    INTUITIVE = "intuitive", _("Intuitive")
    PATIENT = "patient", _("Patient")
    ENERGETIC = "energetic", _("Energetic")
    CALM = "calm", _("Calm")
    ASSERTIVE = "assertive", _("Assertive")
    COLLABORATIVE = "collaborative", _("Collaborative")
    INDEPENDENT = "independent", _("Independent")
    DETAIL_ORIENTED = "detail_oriented", _("Detail-oriented")
    VISIONARY = "visionary", _("Visionary")
    PRAGMATIC = "pragmatic", _("Pragmatic")
    ADAPTIVE = "adaptive", _("Adaptive")
    PRINCIPLED = "principled", _("Principled")
    CURIOUS = "curious", _("Curious")
    DECISIVE = "decisive", _("Decisive")
    REFLECTIVE = "reflective", _("Reflective")
    PROACTIVE = "proactive", _("Proactive")
    SUPPORTIVE = "supportive", _("Supportive")
    CRITICAL_THINKING = "critical_thinking", _("Critical Thinker")
    COMMUNICATIVE = "communicative", _("Communicative")
    RELIABLE = "reliable", _("Reliable")
    INNOVATIVE = "innovative", _("Innovative")


class AgentName(models.TextChoices):
    ALEX = "alex", _("Alex")
    JORDAN = "jordan", _("Jordan")
    CASEY = "casey", _("Casey")
    MORGAN = "morgan", _("Morgan")
    DAKOTA = "dakota", _("Dakota")
    PARKER = "parker", _("Parker")
    TAYLOR = "taylor", _("Taylor")
    BLAKE = "blake", _("Blake")
    RORY = "rory", _("Rory")
    REAGAN = "reagan", _("Reagan")
    BROOKLYN = "brooklyn", _("Brooklyn")
    ARIEL = "ariel", _("Ariel")
    SAGE = "sage", _("Sage")
    PHOENIX = "phoenix", _("Phoenix")
    SKYE = "skye", _("Skye")
    RIVER = "river", _("River")
    CAMERON = "cameron", _("Cameron")
    AVERY = "avery", _("Avery")
    EDEN = "eden", _("Eden")
    HAYDEN = "hayden", _("Hayden")
    ROBIN = "robin", _("Robin")
    PEYTON = "peyton", _("Peyton")
    QUINN = "quinn", _("Quinn")
    TATUM = "tatum", _("Tatum")
    REECE = "reece", _("Reece")


class AgentType(models.TextChoices):
    BASIC = "basic", _("Basic")
    MEDIUM = "medium", _("Medium")
    ADVANCED = "advanced", _("advanced")
