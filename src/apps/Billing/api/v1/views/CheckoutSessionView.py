from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from typing import Any

from ..serializers import CheckoutSessionSerializer
from apps.Common.utils import create_stripe_checkout_session


class CheckoutSessionView(APIView):
    authentication_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = CheckoutSessionSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data: Any = serializer.validated_data
        checkout_session_id = create_stripe_checkout_session(
            success_url=validated_data["success_url"],
            cancel_url=validated_data["cancel_url"],
            stripe_price_id=validated_data["stripe_price_id"],
            customuser_stripe_id=request.user.strip_customer_id,
        )
        return Response(checkout_session_id, status=status.HTTP_200_OK)
