from rest_framework.generics import ListAPIView
from rest_framework.throttling import AnonRateThrottle

from apps.Billing.api.v1.serializers import PriceSerializer
from apps.Billing.models import Price

from rest_framework.permissions import AllowAny


class PriceListView(ListAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = None
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
