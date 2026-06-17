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


class ParticipantStatus(models.TextChoices):
    EN_LINEA = "EN LINEA", _("En linea")
    AUSENTE = "AUSENTE", _("Ausente")
    NO_MOLESTAR = "NO MOLESTAR", _("No molestar")
    INVISIBLE = "INVISIBLE", _("Invisible")


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
    ADVANCE = "advance", _("advance")


class FeatureCode(models.TextChoices):
    BASIC_AGENT = "basic.agent.access", _("Access to the agent type basic")
    MEDIUM_AGENT = "medium.agent.access", _("Acces to the agent type medium")
    ADVANCED_AGENT = "advanced.agent.access", _("Access to the agent type advance")


class ChatType(models.TextChoices):
    AGENT_CHAT = "agent_chat", _("The agent's type")
    USER_CHAT = "user_chat", _("The user's chats")
    USER_GROUP = "user_group", _("The gruops full of user's")
    MIXED_GROUP = "mixed_group", _("The mixed gruop")


class QuotaCode(models.TextChoices):
    AGENT_CHAT_COUNT = "agent.chat.count", _("The amount of chats with agents")
    BASIC_CHAT_COUNT = "basic.chat.count", _("The amount of chats with users")
    GROUP_CHAT_COUNT = "group.chat.count", _("The amount of groups")
    TOKEN_SPEND_MONTHLY = "tokens.spend.monthly", _("The money spend in tokens")
    MAX_PREDICTIONS_MONTHLY = "max.predictions.monthly", _(
        "Max amount of users suggested"
    )


# Client -> Server (Websocket) - which are call commands
class ConversationConsumerCommand(models.TextChoices):
    # STORED DB
    CREATE_MESSAGE = "create_message", _("The user has send a message")
    UPDATE_MESSAGE = "update_message", _("The user has modified a message")
    DELETE_MESSAGE = "delete_message", _("The user has deleted a message")
    READ_MESSAGE = "read_message", _("A message has being read")

    UPDATE_CHAT = "update_chat", _(
        "For update metadata of the chat such as: name, image, description"
    )

    LEFT_PARTICIPANT = "left_participant", _("A participant has left the group")
    JOIN_PARTICIPANT = "join_participant", _("A new participant has joined")

    # WEB-SOCKET ONLY
    START_TYPING = "start_typing", _("A participant start typing")
    STOP_TYPING = "stop_typing", _("A participant stop typing")
    START_RECORDING = "start_recording", _("A participant start recording")
    STOP_RECORDING = "stop_recording", _("A participant stop recording")


# Server -> Client (Websocket) - which are call events
class ConversationConsumerEvent(models.TextChoices):
    # STORED DB
    MESSAGE_CREATED = "message_created"
    MESSAGE_UPDATED = "message_updated"
    MESSAGE_DELETED = "message_deleted"
    MESSAGE_READ = "message_read"

    CHAT_UPDATED = "chat_updated"

    PARTICIPANT_LEFT = "participant_left"
    PARTICIPANT_JOIN = "parcitipant_joined"

    # WEB-SOCKET ONLY
    PARTICIPANT_TYPING = "participant_typing"
