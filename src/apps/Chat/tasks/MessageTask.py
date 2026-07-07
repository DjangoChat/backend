from celery import shared_task
from django.db.models import F
from apps.Chat.models import Chat, Participant, ChatParticipant, MessageStatus, Message


@shared_task(bind=True, max_retries=3)
def create_message_statuses(
    self,
    chat_id,
    participant_id,
    message_id,
):
    try:
        # get info
        chat = Chat.objects.get(pk=chat_id)
        participant = Participant.objects.get(pk=participant_id)
        message = Message.objects.get(pk=message_id)

        # filter participants
        chat_participants = ChatParticipant.objects.filter(chat=chat).exclude(
            participant=participant
        )

        # updated not seen messages
        chat_participants.update(
            not_seen=F("not_seen") + 1,
        )

        # create messages statuses
        messages_statuses = []
        for chat_participant in chat_participants:
            messages_statuses.append(
                MessageStatus(
                    participant=chat_participant.participant,
                    message=message,
                )
            )
        MessageStatus.objects.bulk_create(messages_statuses)

    except Exception as e:
        self.retry(countdown=2, exc=e)
