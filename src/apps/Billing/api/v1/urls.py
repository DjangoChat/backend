from django.urls import path

from apps.Billing.api.v1.views import PlanListView

urlpatterns = [
    path("prices/", PlanListView.as_view(), name="prices-list"),
]
