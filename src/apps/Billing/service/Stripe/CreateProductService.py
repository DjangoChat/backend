from .BaseStripeService import BaseStripeService


class CreateProductService(BaseStripeService):
    def execute(self, name):
        return self.stripe_repo.create_stripe_product(name)
