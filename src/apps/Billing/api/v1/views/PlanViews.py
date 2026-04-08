from rest_framework.generics import ListAPIView

from apps.Billing.api.v1.serializers import PlanSerializer
from apps.Billing.models import Price


def PlanListView(ListAPIView):
    queryset = Price
    serializer_class = PlanSerializer
