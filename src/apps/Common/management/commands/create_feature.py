from typing import Any

from django.core.management.base import BaseCommand
from apps.Common.models import PlanOption, FeatureCode
from apps.Billing.models import Feature, Plan

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
        """Create all features and assign them to plans"""
        self.stdout.write("Creating features...")

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
                self.stdout.write(
                    self.style.ERROR(f"  Plan '{plan_name}' not found. Skipping...")
                )
                continue

            features = Feature.objects.filter(code__in=feature_codes)
            if features.count() != len(feature_codes):
                self.stdout.write(
                    self.style.WARNING(
                        f"  Warning: Not all features found for plan {plan_name}"
                    )
                )

            plan.features.set(features)
            self.stdout.write(
                self.style.SUCCESS(
                    f"  ✓ {plan_name}: {features.count()} features assigned"
                )
            )

        self.stdout.write(self.style.SUCCESS("\n✓ Command completed successfully!"))
