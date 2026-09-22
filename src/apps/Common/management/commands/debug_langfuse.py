from django.conf import settings
from django.core.management.base import BaseCommand

import structlog
from langfuse._client.get_client import get_client

from apps.Chat.repository.OllamaRepository import get_langfuse_handler

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    help = (
        "Send a synthetic trace to Langfuse using the same client the agent "
        "uses, to verify end-to-end ingestion into the Langfuse web UI."
    )

    def handle(self, *args, **options):
        get_langfuse_handler()

        client = get_client()

        logger.info(
            "langfuse_debug_config",
            base_url=settings.LANGFUSE_BASE_URL,
            public_key=settings.LANGFUSE_PUBLIC_KEY,
            secret_key="***" if settings.LANGFUSE_SECRET_KEY else None,
        )

        auth_ok = client.auth_check()
        logger.info("langfuse_auth_check", ok=auth_ok)

        with client.start_as_current_observation(
            name="debug-langfuse",
            as_type="generation",
            input={"message": "debug ping"},
            output={"message": "debug pong"},
        ):
            pass

        client.flush()

        logger.info(
            "langfuse_trace_sent",
            auth_ok=auth_ok,
            trace_url=client.get_trace_url(),
        )
