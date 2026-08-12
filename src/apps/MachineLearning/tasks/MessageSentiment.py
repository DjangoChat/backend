from celery import shared_task

from apps.Chat.models import Message
from transformers import pipeline

clasifier = pipeline(
    "sentiment-analysis",  # type: ignore
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
)


@shared_task(bind=True, max_retries=3)
def create_message_sentiment_analysis(
    self,
    message_id,
):
    try:
        message = Message.objects.get(id=message_id)
        analysis = message.messageanalysis  # type: ignore
        analysis.sentiment = clasifier(message.content)
        analysis.save(update_fields=["sentiment"])

        return {
            "message_id": message_id,
            "status": "success",
        }

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
