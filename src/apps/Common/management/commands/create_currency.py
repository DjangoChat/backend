from typing import Any

from django.core.management.base import BaseCommand

import structlog

from apps.Billing.models import Currency

logger = structlog.get_logger(__name__)


class Command(BaseCommand):

    help = "Command for creating all the currencies"

    def handle(self, *args: Any, **options: Any) -> str | None:

        logger.info("Running command create_currency")

        Currency.objects.get_or_create(
            code="pen",
            name="Sol peruano",
            simbol="S/",
        )
        Currency.objects.get_or_create(
            code="usd",
            name="Dolar estadounidense",
            simbol="$",
        )
