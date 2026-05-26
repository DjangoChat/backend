from typing import Any

from django.core.management.base import BaseCommand
from apps.Common.models import PlanOption, FeatureCode
from apps.Billing.models import Feature, Plan

PLANS = {
    PlanOption.MEMBER: [
        FeatureCode.BASIC_AGENT,
    ],
    PlanOption.PRO: [
        FeatureCode.MEDIUM_AGENT,
    ],
    PlanOption.PREMIUM: [
        FeatureCode.ADVANCED_AGENT,
    ],
}

FEATURES = {
    FeatureCode.BASIC_AGENT: {
        "name": "",
        "description": "",
    },
    FeatureCode.MEDIUM_AGENT: {
        "name": "",
        "description": "",
    },
    FeatureCode.ADVANCED_AGENT: {
        "name": "",
        "description": "",
    },
}


class Command(BaseCommand):

    help = "Command for creating all the features"

    def handle(self, *args: Any, **options: Any) -> str | None:
        """Create all features"""
        for feature_code, feature_data in FEATURES.items():
            Feature.objects.get_or_create(
                code=feature_code,
                defaults={
                    "name": feature_data["name"],
                    "description": feature_data["description"],
                },
            )

        """Assign all the features to the plans"""
        for plan_name, plan_codes in PLANS.items():
            this_plan = Plan.objects.get(name=plan_name)
            list_codes = []
            for code in plan_codes:
                list_codes.append(Feature.objects.get(code=code))
            this_plan.features.add(*list_codes)
