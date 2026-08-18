from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.Billing.api.v1.serializers import (
    CheckoutSessionSerializerInput,
    CheckoutSessionSerializerOutput,
    PriceSerializer,
)

list_price_docs = extend_schema(
    tags=["Price"],
    summary="List available prices",
    description=(
        "Retrieves a list of all available prices/plans. "
        "Public endpoint accessible without authentication. "
        "No pagination applied."
    ),
    responses={
        200: OpenApiResponse(
            response=PriceSerializer(many=True),
            description="List of prices retrieved successfully",
        )
    },
)

create_stripe_session_docs = extend_schema(
    tags=["Stripe"],
    summary="Create Stripe checkout session",
    description=(
        "Creates a Stripe checkout session for subscription payment. "
        "Requires authentication with valid success_url, cancel_url, and stripe_price_id."
    ),
    request=CheckoutSessionSerializerInput,
    responses={
        200: OpenApiResponse(
            response=CheckoutSessionSerializerOutput,
            description="Checkout session created successfully",
        ),
    },
)

webhook_stripe_docs = extend_schema(
    tags=["Stripe"],
    summary="Stripe webhook endpoint",
    description="Receives Stripe webhook events.",
    request=None,
    responses={
        200: OpenApiResponse(description="Webhook processed"),
        400: OpenApiResponse(description="Invalid payload or signature"),
    },
)
