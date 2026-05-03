from django.urls import path

from apps.Billing.api.v1.views import PriceListView, CheckOutSession

urlpatterns = [
    path("prices/", PriceListView.as_view(), name="prices-list"),
    path(
        "stripe/check-out-session/", CheckOutSession.as_view(), name="check-out-session"
    ),
]
