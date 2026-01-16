SPECTACULAR_SETTINGS = {
    "TITLE": "Chat Application",
    "DESCRIPTION": "Practice-oriented chat app with WebSocket support and JWT auth.",
    "VERSION": "1.0.0",
    # Public serving configuration
    "SERVE_PUBLIC": True,
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "SERVE_AUTHENTICATION": None,
    # Path prefix handling and tagging
    "SCHEMA_PATH_PREFIX": "api/v1/",
    "SCHEMA_PATH_PREFIX_TRIM": False,
    "SCHEMA_PATH_PREFIX_INSERT": "",
    # Component and schema generation behavior
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "COMPONENT_SPLIT_PATCH": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": False,
    "ENFORCE_NON_BLANK_FIELDS": False,
    "OAS_VERSION": "3.0.3",
    # UI configuration
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "filter": True,
        "docExpansion": "none",
    },
    "SWAGGER_UI_DIST": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest",
    "SWAGGER_UI_FAVICON_HREF": "https://cdn.jsdelivr.net/npm/swagger-ui-dist@latest/favicon-32x32.png",
    "REDOC_UI_SETTINGS": {
        "expandResponses": "200,201",
        "hideDownloadButton": True,
        "requiredPropsFirst": True,
    },
    "REDOC_DIST": "https://cdn.jsdelivr.net/npm/redoc@latest",
    # Servers metadata
    "SERVERS": [
        {"url": "http://localhost:8000", "description": "Local"},
    ],
    # Global tags / docs
    "TAGS": [],
    "EXTERNAL_DOCS": {},
    "EXTENSIONS_INFO": {},
    "EXTENSIONS_ROOT": {},
    # Authentication exposure control (whitelist shown in schema)
    "AUTHENTICATION_WHITELIST": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "apps.Authentication.authentication.CookieJwtAuth.CookieJwtAuth",
    ],
    # Optional global security (applied to all operations)
    "SECURITY": [
        {"BearerAuth": []},
        {"CookieAuth": []},
    ],
    # Manually append components (e.g., custom auth schemes)
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
            "CookieAuth": {
                "type": "apiKey",
                "in": "cookie",
                "name": "access_token",
                "description": "JWT stored in HTTP-only cookie",
            },
        }
    },
    # Sorting and enums
    "SORT_OPERATIONS": True,
    "ENUM_NAME_OVERRIDES": {
        "ValidationErrorEnum": "drf_standardized_errors.openapi_serializers.ValidationErrorEnum.choices",
        "ClientErrorEnum": "drf_standardized_errors.openapi_serializers.ClientErrorEnum.choices",
        "ServerErrorEnum": "drf_standardized_errors.openapi_serializers.ServerErrorEnum.choices",
        "ErrorCode401Enum": "drf_standardized_errors.openapi_serializers.ErrorCode401Enum.choices",
        "ErrorCode403Enum": "drf_standardized_errors.openapi_serializers.ErrorCode403Enum.choices",
        "ErrorCode404Enum": "drf_standardized_errors.openapi_serializers.ErrorCode404Enum.choices",
        "ErrorCode405Enum": "drf_standardized_errors.openapi_serializers.ErrorCode405Enum.choices",
        "ErrorCode406Enum": "drf_standardized_errors.openapi_serializers.ErrorCode406Enum.choices",
        "ErrorCode415Enum": "drf_standardized_errors.openapi_serializers.ErrorCode415Enum.choices",
        "ErrorCode429Enum": "drf_standardized_errors.openapi_serializers.ErrorCode429Enum.choices",
        "ErrorCode500Enum": "drf_standardized_errors.openapi_serializers.ErrorCode500Enum.choices",
    },
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": True,
    "ENUM_GENERATE_CHOICE_DESCRIPTION": True,
    "ENUM_SUFFIX": "Enum",
    # Ensure standardized error enums/components are properly processed
    "POSTPROCESSING_HOOKS": [
        "drf_standardized_errors.openapi_hooks.postprocess_schema_enums"
    ],
    # Renderers / Parsers exposure (leave None to show all)
    "PARSER_WHITELIST": None,
    "RENDERER_WHITELIST": None,
    # Diagnostics
    "DISABLE_ERRORS_AND_WARNINGS": False,
    "ENABLE_DJANGO_DEPLOY_CHECK": True,
}
