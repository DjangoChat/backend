from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse
from typing import Any

from ..serializers import CheckoutSessionSerializer
from apps.Common.utils import create_stripe_checkout_session


class CheckoutSessionResponseSerializer(serializers.Serializer):
    stripe_session_url = serializers.URLField()


class CheckOutSession(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Billing"],
        summary="Create Stripe checkout session",
        description=(
            "Creates a Stripe checkout session for subscription payment. "
            "Requires authentication with valid success_url, cancel_url, and stripe_price_id."
        ),
        request=CheckoutSessionSerializer,
        responses={
            200: OpenApiResponse(
                response=CheckoutSessionResponseSerializer,
                description="Checkout session created successfully",
            ),
            400: OpenApiResponse(description="Invalid request data"),
        },
    )
    def post(self, request, format=None):
        serializer = CheckoutSessionSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data: Any = serializer.validated_data
        checkout_session = create_stripe_checkout_session(
            success_url=validated_data["success_url"],
            cancel_url=validated_data["cancel_url"],
            stripe_price_id=validated_data["stripe_price_id"],
            customuser_stripe_id=request.user.strip_customer_id,
        )
        return Response(
            data={
                "stripe_session_url": checkout_session.url,
            },
            status=status.HTTP_200_OK,
        )
