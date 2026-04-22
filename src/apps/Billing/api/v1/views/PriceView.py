from rest_framework.generics import ListAPIView

from apps.Billing.api.v1.serializers import PriceSerializer
from apps.Billing.models import Price

from rest_framework.permissions import AllowAny


class PriceListView(ListAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [AllowAny]
