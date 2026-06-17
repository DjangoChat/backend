from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PriceView, StripeView

router = DefaultRouter()
router.register(r"prices", PriceView, basename="price")
router.register(r"stipes", StripeView, basename="stripe")

urlpatterns = [
    path("", include(router.urls)),
]
