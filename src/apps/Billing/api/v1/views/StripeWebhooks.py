from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone as dt_timezone

import stripe
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.Billing.models import Price, Subscription
from apps.Authentication.models import CustomUser
from apps.Common.models import StatusSuscription


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print("Error parsing payload: {}".format(str(e)))
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:  # type: ignore
        print("Error verifying webhook signature: {}".format(str(e)))
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event.type == "customer.subscription.created":
        session = event["data"]["object"]
        stripe_subscription_id = session["id"]
        stripe_customuser_id = session["customer"]
        stripe_price_id = session["items"]["data"][0]["price"]["id"]

        current_price = Price.objects.get(stripe_price_id=stripe_price_id)
        current_customer = CustomUser.objects.get(
            strip_customer_id=stripe_customuser_id
        )

        Subscription.objects.create(
            stripe_subscription_id=stripe_subscription_id,
            user=current_customer,
            price=current_price,
            start_date=datetime.fromtimestamp(
                session["start_date"], tz=dt_timezone.utc
            ),
            current_period_start=datetime.fromtimestamp(
                session["current_period_start"], tz=dt_timezone.utc
            ),
            current_period_end=datetime.fromtimestamp(
                session["current_period_end"], tz=dt_timezone.utc
            ),
            status=StatusSuscription.ACTIVE,
            amount=session["items"]["data"][0]["price"]["unit_amount"],
            currency_code=session["currency"],
            plan_name=current_price.plan.name,
            period_name=current_price.period.name,
        )

    elif event.type == "customer.subscription.updated":
        pass
    elif event.type == "customer.subscription.deleted":
        # canceled suscription
        pass
    else:
        print("Unhandled event type {}".format(event.type))

    return Response(status=status.HTTP_200_OK)
