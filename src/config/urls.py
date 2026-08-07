from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from .views import health_check, readiness_check, liveness_check

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("Authentication.api.v1.urls")),
    path("api/v1/", include("Billing.api.v1.urls")),
    path("api/v1/", include("Chat.api.v1.urls")),
    path("health/", health_check, name="health_check"),
    path("ready/", readiness_check, name="readiness_check"),
    path("live/", liveness_check, name="liveness_check"),
    path("", include("django_prometheus.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "api/schema/",
            SpectacularAPIView.as_view(),
            name="schema",
        ),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path(
            "api/schema/redoc/",
            SpectacularRedocView.as_view(url_name="schema"),
            name="redoc",
        ),
    ]
