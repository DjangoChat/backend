from django.conf import settings

import stripe
import structlog
from stripe._error import APIConnectionError, APIError

stripe.api_key = settings.STRIPE_API_KEY
logger = structlog.get_logger(__name__)


class StripeRepository:

    def create_customer(self, name, email, phone):
        try:
            return stripe.Customer.create(
                name=name,
                email=email,
                phone=phone,
            )
        except (APIConnectionError, APIError) as e:
            logger.error(
                "stripe_create_cutomer_failed",
                email=email,
                reason=e,
            )
            raise

    def create_stripe_product(self, name):
        try:
            return stripe.Product.create(
                name=name,
            )
        except (APIConnectionError, APIError) as e:
            logger.error(
                "stripe_create_product_failed",
                name=name,
                reason=e,
            )
            raise

    def create_stripe_price(self, currency, unit_amount, months, product_id):
        try:
            return stripe.Price.create(
                currency=currency,
                unit_amount=unit_amount,
                recurring={"interval": "month", "interval_count": months},
                product=product_id,
            )
        except (APIConnectionError, APIError) as e:
            logger.error(
                "stripe_create_price_failed",
                product_id=product_id,
                reason=e,
            )
            raise

    def create_stripe_checkout_session(
        self, success_url, cancel_url, stripe_price_id, customuser_stripe_id
    ):
        try:
            return stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=cancel_url,
                line_items=[
                    {
                        "price": stripe_price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                customer=customuser_stripe_id,
            )
        except (APIConnectionError, APIError) as e:
            logger.error(
                "stripe_create_checkout_session_failed",
                stripe_price_id=stripe_price_id,
                customuser_stripe_id=customuser_stripe_id,
                reason=e,
            )
            raise
