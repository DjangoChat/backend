import structlog
from celery import shared_task
from sentence_transformers import SentenceTransformer

from apps.Chat.models import Message

logger = structlog.get_logger(__name__)
_model = None


def get_model():
    """Lazy load the embedding model on first use."""
    global _model
    if _model is None:
        _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    return _model


@shared_task(bind=True, max_retries=3)
def create_message_embedding(
    self,
    message_id,
):
    try:
        message = Message.objects.get(id=message_id)
        model = get_model()
        embedding = model.encode(message.content)

        analysis = message.messageanalysis  # type: ignore
        analysis.embedding = embedding.tolist()
        analysis.save(update_fields=["embedding"])

        data = {
            "message_id": message_id,
            "action": "create_message_embedding",
            "embedding": analysis.embedding,
            "status": "success",
        }

        logger.info("message_analysis", **data)
        return data

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
