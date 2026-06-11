from apps.Billing.repository import StripeRepository


class BaseStripeService:

    def __init__(self):
        self.stripe_repo = StripeRepository()
