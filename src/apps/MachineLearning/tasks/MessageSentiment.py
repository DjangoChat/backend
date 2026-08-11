from celery import shared_task


@shared_task(bind=True, max_retries=3)
def create_message_sentiment_analysis(
    self,
    message_content: str,
):
    try:
        pass

    except Exception as e:
        self.retry(countdown=2, exc=e)
