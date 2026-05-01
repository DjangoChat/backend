from typing import Any

from django.core.management.base import BaseCommand


from apps.Billing.models import Currency, Period, Plan, Price
from apps.Common.models import Frequency, PlanOption
from apps.Common.utils import create_stripe_price


PRICE = {
    PlanOption.MEMBER: 700,
    PlanOption.PRO: 1200,
    PlanOption.PREMIUM: 1700,
}

DISCOUNT = {
    Frequency.MONTHLY: 0,
    Frequency.TRIMESTER: 5,
    Frequency.ANNUAL: 7,
}


class Command(BaseCommand):

    help = "Command for creating all the prices"

    def create_stripe_price(
        self, price: Price, produc_id: str | None, currency_code: str, months: int
    ) -> None:
        if produc_id is not None:
            new_price = create_stripe_price(
                currency=currency_code,
                unit_amount=price.amount,
                months=months,
                product_id=produc_id,
            )
            price.stripe_price_id = new_price.id
            price.save()

    def handle(self, *args: Any, **options: Any) -> str | None:

        self.stdout.write("CREATING PRICES COMMAND RUNNING")
        actual_currency = Currency.objects.get(code="usd")

        for opt in PlanOption:
            current_plan = Plan.objects.get(name=opt)

            for freq in Frequency:
                current_period = Period.objects.get(name=freq)

                new_price, created = Price.objects.get_or_create(
                    plan=current_plan,
                    period=current_period,
                    currency=actual_currency,
                    amount=(
                        PRICE[opt]
                        * current_period.interval_count
                        * (100 - DISCOUNT[freq])
                        // 100
                    ),
                )

                if created:
                    self.create_stripe_price(
                        new_price,
                        current_plan.stripe_product_id,
                        actual_currency.code,
                        current_period.interval_count,
                    )
