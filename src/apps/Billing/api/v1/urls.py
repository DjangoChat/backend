from django.urls import path, include
from .views import PriceView, StripeView

urlpatterns = [
    path(
        "prices/",
        PriceView.as_view({"get": "list"}),
    ),
    path(
        "stripe/",
        include(
            [
                path(
                    "create-session/",
                    StripeView.as_view({"post": "create_session"}),
                ),
                path(
                    "webhook/",
                    StripeView.as_view({"post": "webhook"}),
                ),
            ]
        ),
    ),
]
