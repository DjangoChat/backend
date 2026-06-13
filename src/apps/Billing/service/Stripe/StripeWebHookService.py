import logging
from datetime import datetime
from datetime import timezone as dt_timezone

from django.conf import settings

import stripe
from rest_framework import status

from apps.Authentication.models import CustomUser
from apps.Billing.models import Price, Subscription
from apps.Common.models import StatusSuscription


class StripeWebHookService:
    logger = logging.getLogger(__name__)

    def execute(
        self,
        payload,
        sig_header,
    ):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            self.logger.error("Error parsing payload: {}".format(str(e)))
            return status.HTTP_400_BAD_REQUEST
        except stripe.error.SignatureVerificationError as e:  # type: ignore
            self.logger.error("Error verifying webhook signature: {}".format(str(e)))
            return status.HTTP_400_BAD_REQUEST

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

        return status.HTTP_200_OK
