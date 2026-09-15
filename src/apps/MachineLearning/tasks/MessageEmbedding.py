from celery import shared_task
from sentence_transformers import SentenceTransformer

from apps.Chat.models import Message

# Lazy-load model to avoid downloading on startup
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

        return {
            "message_id": message_id,
            "status": "success",
        }

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
