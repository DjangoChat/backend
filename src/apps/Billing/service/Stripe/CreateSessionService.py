from .BaseStripeService import BaseStripeService


class CreateSessionService(BaseStripeService):
    def execute(self, success_url, cancel_url, stripe_price_id, customuser_stripe_id):
        return self.stripe_repo.create_stripe_checkout_session(
            success_url, cancel_url, stripe_price_id, customuser_stripe_id
        )
