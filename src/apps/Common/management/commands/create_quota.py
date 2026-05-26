from typing import Any

from django.core.management.base import BaseCommand
from apps.Common.models import QuotaCode
from apps.Billing.models import Quota

QUOTAS = {
    QuotaCode.AGENT_CHAT_COUNT: {
        "name": "",
        "description": "",
    },
    QuotaCode.BASIC_CHAT_COUNT: {
        "name": "",
        "description": "",
    },
    QuotaCode.GROUP_CHAT_COUNT: {
        "name": "",
        "description": "",
    },
    QuotaCode.TOKEN_SPEND_MONTHLY: {
        "name": "",
        "description": "",
    },
    QuotaCode.MAX_PREDICTIONS_MONTHLY: {
        "name": "",
        "description": "",
    },
}


class Command(BaseCommand):

    help = "Command for creating all the quotas definition's"

    def handle(self, *args: Any, **options: Any) -> str | None:
        for quota_name, quota_data in QUOTAS.items():
            Quota.objects.get_or_create(
                name=quota_name,
                defaults={
                    "name": quota_data["name"],
                    "description": quota_data["description"],
                },
            )
