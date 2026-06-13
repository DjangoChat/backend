from django.conf import settings

import stripe
from rest_framework import serializers

stripe.api_key = settings.STRIPE_API_KEY


class CheckoutSessionSerializerInput(serializers.Serializer):
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()
    stripe_price_id = serializers.CharField()


class CheckoutSessionSerializerOutput(serializers.Serializer):
    stripe_session_url = serializers.URLField()
