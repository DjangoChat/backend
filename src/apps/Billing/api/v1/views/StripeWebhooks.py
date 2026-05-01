from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import stripe
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
        pass
    elif event.type == "customer.subscription.updated":
        pass
    elif event.type == "customer.subscription.deleted":
        # canceled suscription
        pass
    else:
        print("Unhandled event type {}".format(event.type))

    return Response(status=status.HTTP_200_OK)
