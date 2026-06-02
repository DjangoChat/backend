from rest_framework.generics import ListAPIView
from rest_framework.throttling import AnonRateThrottle
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.permissions import AllowAny

from apps.Billing.api.v1.serializers import PriceSerializer
from apps.Billing.models import Price


class PriceListView(ListAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = None
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    @extend_schema(
        tags=["Billing"],
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
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
