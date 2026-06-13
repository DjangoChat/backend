import logging

from django.conf import settings

import stripe
from stripe._error import APIConnectionError, APIError

stripe.api_key = settings.STRIPE_API_KEY


class StripeRepository:
    logger = logging.getLogger(__name__)

    def create_customer(self, name, email, phone):
        try:
            return stripe.Customer.create(
                name=name,
                email=email,
                phone=phone,
            )
        except APIConnectionError as e:
            self.logger.error(f"Stripe connection error creating customer: {str(e)}")
            raise
        except APIError as e:
            self.logger.error(f"Stripe API error creating customer: {str(e)}")
            raise

    def create_stripe_product(self, name):
        try:
            return stripe.Product.create(
                name=name,
            )
        except APIConnectionError as e:
            self.logger.error(f"Stripe connection error creating product: {str(e)}")
            raise
        except APIError as e:
            self.logger.error(f"Stripe API error creating product: {str(e)}")
            raise

    def create_stripe_price(self, currency, unit_amount, months, product_id):
        try:
            return stripe.Price.create(
                currency=currency,
                unit_amount=unit_amount,
                recurring={"interval": "month", "interval_count": months},
                product=product_id,
            )
        except APIConnectionError as e:
            self.logger.error(f"Stripe connection error creating price: {str(e)}")
            raise
        except APIError as e:
            self.logger.error(f"Stripe API error creating price: {str(e)}")
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
        except APIConnectionError as e:
            self.logger.error(
                f"Stripe connection error creating checkout session: {str(e)}"
            )
            raise
        except APIError as e:
            self.logger.error(f"Stripe API error creating checkout session: {str(e)}")
            raise
