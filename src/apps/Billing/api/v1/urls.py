from django.urls import path
from .views import PriceView, StripeView

urlpatterns = [
    path(
        "prices/",
        PriceView.as_view({"get": "list"}),
    ),
    path(
        "stripe/create-session/",
        StripeView.as_view({"post": "create_session"}),
    ),
    path(
        "stripe/webhook/",
        StripeView.as_view({"post": "webhook"}),
    ),
]
