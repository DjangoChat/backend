from typing import cast

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.Billing.api.v1.docs import create_stripe_session_docs, webhook_stripe_docs
from apps.Billing.service import CreateSessionService, StripeWebHookService

from ..serializers import (
    CheckoutSessionSerializerInput,
    CheckoutSessionSerializerOutput,
)


class StripeView(viewsets.ViewSet):

    @create_stripe_session_docs
    @action(
        detail=False,
        methods=["post"],
    )
    def create_session(self, request):
        serializer = CheckoutSessionSerializerInput(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = cast(dict, serializer.validated_data)

        checkout_session = CreateSessionService().execute(
            success_url=validated_data["success_url"],
            cancel_url=validated_data["cancel_url"],
            stripe_price_id=validated_data["stripe_price_id"],
            customuser_stripe_id=request.user.strip_customer_id,
        )
        response = CheckoutSessionSerializerOutput(
            {"stripe_session_url": checkout_session.url}
        )
        return Response(response.data, status=status.HTTP_200_OK)

    @webhook_stripe_docs
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
    )
    @method_decorator(csrf_exempt)
    def webhook(self, request):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        response_status = StripeWebHookService().execute(payload, sig_header)
        return Response(status=response_status)
