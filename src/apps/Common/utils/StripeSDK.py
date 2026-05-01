from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_customuser(name, email, phone):
    return stripe.Customer.create(
        name=name,
        email=email,
        phone=phone,
    )


def create_stripe_product(name):
    return stripe.Product.create(
        name=name,
    )


def create_stripe_price(currency, unit_amount, months, product_id):
    return stripe.Price.create(
        currency=currency,
        unit_amount=unit_amount,
        recurring={"interval": "month", "interval_count": months},
        product=product_id,
    )


def create_stripe_checkout_session(
    success_url, cancel_url, stripe_price_id, customuser_stripe_id
):
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
