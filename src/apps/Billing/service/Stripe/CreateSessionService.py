from django.shortcuts import get_object_or_404

from .BaseStripeService import BaseStripeService
from apps.Billing.models import Price


class CreateSessionService(BaseStripeService):
    def execute(self, success_url, cancel_url, stripe_price_id, customuser_stripe_id):
        price = get_object_or_404(Price, id=stripe_price_id)
        return self.stripe_repo.create_stripe_checkout_session(
            success_url,
            cancel_url,
            price.stripe_price_id,
            customuser_stripe_id,
        )
