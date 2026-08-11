from django.db import models
from django.utils.translation import gettext_lazy as _
from pgvector.django import VectorField

from apps.Common.models import CustomModel


class MessageAnalysis(CustomModel):
    message = models.OneToOneField(
        "Message",
        on_delete=models.CASCADE,
    )
    sentiment = models.FloatField(
        _("Sentiment analysis from roBERTa"),
        null=True,
        blank=True,
    )
    emotions = models.JSONField(
        _("Emotions analysis of GoEmotions"),
        default=dict,
        null=True,
        blank=True,
    )
    topics = models.JSONField(
        _("Topic extraction from BERTopic"),
        default=dict,
        null=True,
        blank=True,
    )
    embedding = VectorField(
        _("Embedding from the text"),
        dimensions=384,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "MACHINE_LEARNING_MESSAGE_ANALYSIS"
        verbose_name = _("Message Analysis")
        verbose_name_plural = _("Messages Analysis")
        app_label = "MachineLearning"
