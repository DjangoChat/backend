import structlog
from celery import shared_task
from transformers import pipeline

from apps.Chat.models import Message

logger = structlog.get_logger(__name__)
_classifier = None


def get_classifier():
    """Lazy load the emotion classifier on first use."""
    global _classifier
    if _classifier is None:
        _classifier = pipeline(
            "text-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            return_all_scores=True,
        )
    return _classifier


@shared_task(bind=True, max_retries=3)
def create_message_emotion_analysis(
    self,
    message_id,
):
    try:
        message = Message.objects.get(id=message_id)
        analysis = message.messageanalysis  # type: ignore
        classifier = get_classifier()
        analysis.emotions = classifier(message.content)
        analysis.save(update_fields=["emotions"])

        data = {
            "message_id": message_id,
            "action": "create_message_emotion_analysis",
            "emotions": analysis.emotions,
            "status": "success",
        }

        logger.info("message_analysis", **data)
        return data

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
