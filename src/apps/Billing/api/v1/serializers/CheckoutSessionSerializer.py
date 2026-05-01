from django.conf import settings
from rest_framework import serializers

import stripe

stripe.api_key = settings.STRIPE_API_KEY


class CheckoutSessionSerializer(serializers.Serializer):
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()
    stripe_price_id = serializers.CharField()
