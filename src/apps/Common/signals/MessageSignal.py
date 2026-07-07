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
