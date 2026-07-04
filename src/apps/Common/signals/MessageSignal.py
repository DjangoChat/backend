from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.Chat.models import ChatParticipant, Message, MessageStatus
from apps.Chat.service import OllamaChatService
from apps.Common.models import MessageType


# TODO: eventually move this to the websocket to get inmediate response
@receiver(post_save, sender=Message)
def create_agent_response(sender, instance, created, **kwargs):
    if created and instance.participant.agent:
        response = OllamaChatService().execute(
            chat=instance.chat,
            prompt_type=instance.agent.promp_type,
        )
        agent_participant = (
            ChatParticipant.objects.filter(chat=instance.chat)
            .exclude(participant=instance.participant)
            .first()
        )
        Message.objects.create(
            chat=instance.chat,
            participant=agent_participant,
            message_type=MessageType.TEXT,
            content=response,
        )


@receiver(post_save, sender=Message)
def create_messages_statuses(sender, instance, created, **kwargs):
    if created:
        chat_participants = ChatParticipant.objects.filter(
            chat=instance.chat,
        ).exclude(
            participant=instance.participant,
        )
        for chat_participant in chat_participants:
            MessageStatus.objects.create(
                participant=chat_participant.participant,
                message=instance,
            )


@receiver(post_save, sender=Message)
def update_chat_last_message(sender, instance, created, **kwargs):
    if created:
        instance.chat.last_message_at = instance.sent_at
        instance.chat.save(update_fields=["last_message_at"])
