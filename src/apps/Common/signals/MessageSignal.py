import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from apps.Chat.api.v1.serializers import (
    ChatDetailedSerializer,
    MessageDetailedSerializer,
)
from apps.Chat.models import ChatParticipant, Message
from apps.Common.models import ParticipantType
from apps.MachineLearning.models import MessageAnalysis
from apps.MachineLearning.tasks import (
    create_message_embedding,
    create_message_emotion_analysis,
    create_message_sentiment_analysis,
    create_message_topic_analysis,
)


# TODO: Re-enable when notification consumer logic is ready
@receiver(post_save, sender=Message)
def send_notification_notificationconsumer(sender, instance, created, **kwargs):
    if not created:
        return

    chat = instance.chat
    participant = instance.participant

    channel_layer = get_channel_layer()

    users_to_be_notified = (
        ChatParticipant.objects.filter(
            chat=chat,
        )
        .exclude(
            participant=participant.id,
        )
        .exclude(
            participant__participant_type=ParticipantType.AGENT,
        )
        .values_list(
            "participant__user_id",
            flat=True,
        )
    )

    for user_id in users_to_be_notified:
        group_name = f"notification__{user_id}"
        serialized_data = json.loads(
            json.dumps(ChatDetailedSerializer(chat).data, cls=DjangoJSONEncoder)
        )
        payload = {
            "type": "chat_message",
            "data": serialized_data,
        }

        async_to_sync(channel_layer.group_send)(group_name, payload)  # type: ignore


@receiver(post_save, sender=Message)
def send_notification_chatconsumer(sender, instance, created, **kwargs):
    if not created:
        return

    chat_id = instance.chat.id

    channel_layer = get_channel_layer()

    group_name = f"chat_room__{chat_id}"
    serialized_data = json.loads(
        json.dumps(MessageDetailedSerializer(instance).data, cls=DjangoJSONEncoder)
    )
    payload = {
        "type": "chat_message",
        "data": serialized_data,
    }

    async_to_sync(channel_layer.group_send)(group_name, payload)  # type: ignore


@receiver(post_save, sender=Message)
def create_message_analysis(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.participant.agent:
        return

    MessageAnalysis.objects.create(message=instance)
    message_id = instance.id

    transaction.on_commit(
        lambda: (
            create_message_emotion_analysis.delay(message_id),
            create_message_sentiment_analysis.delay(message_id),
            create_message_embedding.delay(message_id),
            create_message_topic_analysis.delay(message_id),
        )
    )
