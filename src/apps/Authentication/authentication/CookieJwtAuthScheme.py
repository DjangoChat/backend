from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CookieJwtAuthScheme(OpenApiAuthenticationExtension):
    """
    OpenAPI extension for CookieJwtAuth.

    This extension tells drf-spectacular how to represent the custom
    CookieJwtAuth authentication class in the OpenAPI schema.
    """

    target_class = "apps.Authentication.authentication.CookieJwtAuth.CookieJwtAuth"
    name = "CookieAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
            "description": "JWT stored in HTTP-only cookie",
        }
