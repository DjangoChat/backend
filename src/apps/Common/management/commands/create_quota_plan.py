from typing import Any

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from apps.Common.models import QuotaCode, PlanOption
from apps.Billing.models import Quota, Plan, QuotaPlan

QUOTAS = [
    (QuotaCode.AGENT_CHAT_COUNT, PlanOption.MEMBER, 5),
    (QuotaCode.AGENT_CHAT_COUNT, PlanOption.PRO, 15),
    (QuotaCode.AGENT_CHAT_COUNT, PlanOption.PREMIUM, 25),
    (QuotaCode.MAX_PREDICTIONS_MONTHLY, PlanOption.MEMBER, 10),
    (QuotaCode.MAX_PREDICTIONS_MONTHLY, PlanOption.PRO, 20),
    (QuotaCode.MAX_PREDICTIONS_MONTHLY, PlanOption.PREMIUM, 40),
    (QuotaCode.TOKEN_SPEND_MONTHLY, PlanOption.MEMBER, 6),
    (QuotaCode.TOKEN_SPEND_MONTHLY, PlanOption.PRO, 10),
    (QuotaCode.TOKEN_SPEND_MONTHLY, PlanOption.PREMIUM, 14),
]


class Command(BaseCommand):

    help = "Command for creating all the relations between quota and plan"

    def handle(self, *args: Any, **options: Any) -> str:
        try:
            quota_plans = []
            for quota_code, plan_option, limit in QUOTAS:
                try:
                    quota = Quota.objects.get(code=quota_code)
                except Quota.DoesNotExist:
                    raise CommandError(f"Quota with code '{quota_code}' does not exist")

                try:
                    plan = Plan.objects.get(name=plan_option)
                except Plan.DoesNotExist:
                    raise CommandError(f"Plan with name '{plan_option}' does not exist")

                quota_plans.append(QuotaPlan(quota=quota, plan=plan, limit=limit))

            QuotaPlan.objects.bulk_create(quota_plans, ignore_conflicts=True)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {len(quota_plans)} quota-plan relations"
                )
            )
            return "Success"
        except CommandError as e:
            self.stderr.write(self.style.ERROR(f"Error: {str(e)}"))
            raise
