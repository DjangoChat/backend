from .BaseStripeService import BaseStripeService


class CreatePriceService(BaseStripeService):
    def execute(self, currency, unit_amount, months, product_id):
        return self.stripe_repo.create_stripe_price(
            currency, unit_amount, months, product_id
        )
