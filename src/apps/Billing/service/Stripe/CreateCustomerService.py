from .BaseStripeService import BaseStripeService


class CreateCustomerService(BaseStripeService):
    def execute(self, name, email, phone):
        return self.stripe_repo.create_customer(name, email, phone)
