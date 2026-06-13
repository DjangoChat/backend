from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from apps.Billing.api.v1.docs import list_price_docs
from apps.Billing.api.v1.serializers import PriceSerializer
from apps.Billing.models import Price


class PriceView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    @list_price_docs
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
