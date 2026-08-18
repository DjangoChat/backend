from typing import Any
import structlog

from django.core.management.base import BaseCommand

from apps.Billing.models import Feature, Plan
from apps.Common.models import FeatureCode, PlanOption

logger = structlog.get_logger(__name__)

PLANS = {
    PlanOption.MEMBER: [
        FeatureCode.BASIC_AGENT,
    ],
    PlanOption.PRO: [
        FeatureCode.BASIC_AGENT,
        FeatureCode.MEDIUM_AGENT,
    ],
    PlanOption.PREMIUM: [
        FeatureCode.BASIC_AGENT,
        FeatureCode.MEDIUM_AGENT,
        FeatureCode.ADVANCED_AGENT,
    ],
}

FEATURES = {
    FeatureCode.BASIC_AGENT: {
        "name": "Basic Agent",
        "description": "Access to basic AI agent capabilities with standard features",
    },
    FeatureCode.MEDIUM_AGENT: {
        "name": "Medium Agent",
        "description": "Access to medium-tier AI agent with enhanced capabilities",
    },
    FeatureCode.ADVANCED_AGENT: {
        "name": "Advanced Agent",
        "description": "Access to advanced AI agent with full feature set and priority support",
    },
}


class Command(BaseCommand):
    help = "Create all features and assign them to plans"

    def handle(self, *args: Any, **options: Any) -> None:
        logger.info("Running command create_feature")

        # Create features
        for feature_code, feature_data in FEATURES.items():
            feature, created = Feature.objects.get_or_create(
                code=feature_code,
                defaults={
                    "name": feature_data["name"],
                    "description": feature_data["description"],
                },
            )

        # Assign features to plans
        for plan_name, feature_codes in PLANS.items():
            try:
                plan = Plan.objects.get(name=plan_name)
            except Plan.DoesNotExist:
                logger.error(
                    "create_feature_failed",
                    reason=f"Plan {plan_name} does not exists",
                )
                continue

            features = Feature.objects.filter(code__in=feature_codes)
            plan.features.set(features)
