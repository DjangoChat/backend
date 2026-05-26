REST_FRAMEWORK = {
    # VERSIONING
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_VERSION": "v1",
    "ALLOWED_VERSIONS": ("v1",),
    "VERSION_PARAM": "version",
    # THROTTLE
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "50/day",
        "user": "1000/day",
        "auth": "5/min",
        "refresh": "12/hour",
    },
    # PAGINATION
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 50,
    # AUTHENTICATION
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.Authentication.authentication.CookieJwtAuth",
    ],
    # SCHEMA
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    # EXCEPTION
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    # FILTERING
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
