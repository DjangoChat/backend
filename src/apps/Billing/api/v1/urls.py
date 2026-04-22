from django.urls import path

from apps.Billing.api.v1.views import PriceListView

urlpatterns = [
    path("prices/", PriceListView.as_view(), name="prices-list"),
]
