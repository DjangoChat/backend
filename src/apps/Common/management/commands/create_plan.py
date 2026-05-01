from typing import Any

from django.core.management.base import BaseCommand


from apps.Billing.models import Plan
from apps.Common.models import PlanOption
from apps.Common.utils import create_stripe_product


class Command(BaseCommand):

    help = "Command for creating all the plans"

    def create_stripe_product(self, product: Plan) -> None:
        new_product = create_stripe_product(
            name=product.name,
        )
        product.stripe_product_id = new_product.id
        product.save()

    def handle(self, *args: Any, **options: Any) -> str | None:

        self.stdout.write("CREATING PLAN COMMAND RUNNING")

        for option in PlanOption:
            new_plane, created = Plan.objects.get_or_create(
                name=option,
                description=f"{option.capitalize()} Plan",
            )
            if created:
                self.create_stripe_product(new_plane)
