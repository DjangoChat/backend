from typing import Any

from django.core.management.base import BaseCommand

from apps.Billing.models import Period
from apps.Common.models import Frequency


class Command(BaseCommand):

    help = "Command for creating all the periods"

    def handle(self, *args: Any, **options: Any) -> str | None:
        Period.objects.get_or_create(
            name=Frequency.MONTHLY,
            interval_count=1,
        )
        Period.objects.get_or_create(
            name=Frequency.TRIMESTER,
            interval_count=3,
        )
        Period.objects.get_or_create(
            name=Frequency.ANNUAL,
            interval_count=12,
        )
