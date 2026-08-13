from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.Chat.models import ChatParticipant, Message
from apps.MachineLearning.models import MessageAnalysis
from apps.MachineLearning.tasks import (
    create_message_topic_analysis,
    create_message_sentiment_analysis,
    create_message_emotion_analysis,
    create_message_embedding,
)
from apps.Common.models import ParticipantType
from apps.Chat.api.v1.serializers import (
    ChatDetailedSerializer,
    MessageDetailedSerializer,
)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
            participant=participant,
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
        payload = (
            {
                "type": "chat_message",
                "data": ChatDetailedSerializer(chat).data,
            },
        )

        async_to_sync(channel_layer.group_send)(group_name, payload)  # type: ignore


@receiver(post_save, sender=Message)
def send_notification_chatconsumer(sender, instance, created, **kwargs):
    if not created:
        return

    chat_id = instance.chat.id

    channel_layer = get_channel_layer()
    group_name = f"chat_room__{chat_id}"
    payload = (
        {
            "type": "chat_message",
            "data": MessageDetailedSerializer(instance).data,
        },
    )

    async_to_sync(channel_layer.group_send)(group_name, payload)  # type: ignore


@receiver(post_save, sender=Message)
def create_message_analysis(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.participant.agent:
        return

    messageML = MessageAnalysis.objects.create(message=instance)
    message_id = messageML.id

    create_message_emotion_analysis.delay(message_id)  # type: ignore
    create_message_sentiment_analysis.delay(message_id)  # type: ignore
    create_message_embedding(message_id)  # type: ignore
    create_message_topic_analysis.delay(message_id)  # type: ignore
