from typing import Any

from django.core.management.base import BaseCommand

from apps.Billing.models import Quota
from apps.Common.models import QuotaCode

QUOTAS = {
    QuotaCode.AGENT_CHAT_COUNT: {
        "name": "Agent Chat Count",
        "description": "Maximum number of agent conversations allowed per month",
    },
    QuotaCode.BASIC_CHAT_COUNT: {
        "name": "Basic Chat Count",
        "description": "Maximum number of basic chat interactions allowed per month",
    },
    QuotaCode.GROUP_CHAT_COUNT: {
        "name": "Group Chat Count",
        "description": "Maximum number of group chat sessions allowed per month",
    },
    QuotaCode.TOKEN_SPEND_MONTHLY: {
        "name": "Monthly Token Spend",
        "description": "Maximum number of tokens allowed to spend per month",
    },
    QuotaCode.MAX_PREDICTIONS_MONTHLY: {
        "name": "Maximum Predictions Monthly",
        "description": "Maximum number of predictions allowed per month",
    },
}


class Command(BaseCommand):

    help = "Command for creating all the quotas definition's"

    def handle(self, *args: Any, **options: Any) -> str | None:
        for quota_code, quota_data in QUOTAS.items():
            Quota.objects.get_or_create(
                code=quota_code,
                defaults={
                    "name": quota_data["name"],
                    "description": quota_data["description"],
                },
            )
