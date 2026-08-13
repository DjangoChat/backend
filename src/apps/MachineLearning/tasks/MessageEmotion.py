from celery import shared_task

from apps.Chat.models import Message
from transformers import pipeline

# Lazy-load classifier to avoid downloading model on startup
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

        return {
            "message_id": message_id,
            "status": "success",
        }

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
