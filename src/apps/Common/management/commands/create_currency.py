from typing import Any

from django.core.management.base import BaseCommand

from apps.Billing.models import Currency


class Command(BaseCommand):

    help = "Command for creating all the currencies"

    def handle(self, *args: Any, **options: Any) -> str | None:

        self.stdout.write("CREATING CURRENCY COMMAND RUNNING")

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
