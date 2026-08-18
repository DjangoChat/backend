from celery import shared_task

from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer

from apps.Chat.models import Message


@shared_task(bind=True, max_retries=3)
def create_message_topic_analysis(
    self,
    message_id,
):
    try:
        message = Message.objects.get(id=message_id)
        analysis = message.messageanalysis  # type: ignore
        documents = [message.content]
        embeddings = [analysis.embedding]

        umap_model = UMAP(
            n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric="cosine",
            random_state=42,
        )

        hdbscan_model = HDBSCAN(
            min_cluster_size=10,
            metric="euclidean",
            cluster_selection_method="eom",
            prediction_data=True,
        )

        vectorizer_model = CountVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )

        ctfidf_model = ClassTfidfTransformer()

        representation_model = KeyBERTInspired()

        topic_model = BERTopic(
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            vectorizer_model=vectorizer_model,
            ctfidf_model=ctfidf_model,
            representation_model=representation_model,
        )

        topics, probabilities = topic_model.fit_transform(
            documents=documents,
            embeddings=embeddings,  # type: ignore
        )

        analysis.topics = topics
        analysis.save(update_fields=["topics"])

    except Exception as e:
        self.retry(countdown=2, exc=e)
