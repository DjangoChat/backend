import structlog
from celery import shared_task
from transformers import pipeline

from apps.Chat.models import Message

logger = structlog.get_logger(__name__)
_classifier = None


def get_classifier():
    """Lazy load the sentiment classifier on first use."""
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "sentiment-analysis",  # type: ignore
            model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        )
    return _classifier


@shared_task(bind=True, max_retries=3)
def create_message_sentiment_analysis(
    self,
    message_id,
):
    try:
        message = Message.objects.get(id=message_id)
        analysis = message.messageanalysis  # type: ignore
        classifier = get_classifier()
        analysis.sentiment = classifier(message.content)[0]["score"]
        analysis.save(update_fields=["sentiment"])

        data = {
            "message_id": message_id,
            "action": "create_message_sentiment_analysis",
            "sentiment": analysis.sentiment,
            "status": "success",
        }

        logger.info("message_analysis", **data)
        return data

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
