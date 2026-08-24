from celery import shared_task

from keybert import KeyBERT

from apps.Chat.models import Message
from apps.MachineLearning.tasks.MessageEmbedding import get_model

# Lazy-load KeyBERT, reusing the SentenceTransformer already in memory
_kw_model = None


def get_kw_model():
    """Lazy-load KeyBERT, sharing the embedding model already loaded."""
    global _kw_model
    if _kw_model is None:
        _kw_model = KeyBERT(model=get_model())
    return _kw_model


@shared_task(bind=True, max_retries=3)
def create_message_topic_analysis(
    self,
    message_id,
):
    try:
        message = Message.objects.get(id=message_id)
        analysis = message.messageanalysis  # type: ignore

        kw_model = get_kw_model()
        keywords = kw_model.extract_keywords(
            message.content,
            keyphrase_ngram_range=(1, 2),
            stop_words="english",
            top_n=5,
        )

        # Store as list of {"keyword": str, "score": float}
        analysis.topics = [
            {"keyword": kw, "score": round(score, 4)} for kw, score in keywords
        ]
        analysis.save(update_fields=["topics"])

        return {"message_id": message_id, "status": "success"}

    except Message.DoesNotExist:
        raise

    except Exception as e:
        self.retry(countdown=2, exc=e)
