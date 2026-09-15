from celery import shared_task

from apps.Chat.models import Chat, Message, Participant
from apps.Chat.service.CreateAgentResponseService import CreateAgentResponseService


@shared_task(bind=True, max_retries=3)
def create_agent_response(
    self,
    id_chat,
    id_message,
    id_participant,
):
    try:
        chat = Chat.objects.get(id=id_chat)
        message = Message.objects.get(id=id_message)
        participant = Participant.objects.get(id=id_participant)

        CreateAgentResponseService().execute(
            chat=chat,
            message=message,
            participant=participant,
        )

    except Chat.DoesNotExist:
        raise

    except Message.DoesNotExist:
        raise

    except Participant.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
