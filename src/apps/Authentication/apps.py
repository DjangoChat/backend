from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.Authentication"

    def ready(self):
        # Import the OpenAPI extension so drf-spectacular discovers it
        from apps.Authentication.authentication import CookieJwtAuthScheme  # noqa: F401
