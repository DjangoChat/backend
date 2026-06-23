import os
import sys
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ====================================
# BASIC CONFIG
# ====================================

APPS_DIRS = os.path.join(BASE_DIR, "apps")
FIXTURES_DIRS = os.path.join(BASE_DIR, "fixtures")

if APPS_DIRS not in sys.path:
    sys.path.insert(0, APPS_DIRS)

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "Authentication.CustomUser"

CSRF_COOKIE_HTTPONLY = os.environ.get("CSRF_COOKIE_HTTPONLY", "True") == "True"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", "True") == "True"
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", "*").split(",")

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

# ====================================
# APPS
# ====================================

DJANGO_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "phonenumber_field",
    "corsheaders",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_standardized_errors",
    "django_filters",
]

PERSONAL_APPS = [
    "Authentication.apps.AuthenticationConfig",
    "Authorization.apps.AuthorizationConfig",
    "Chat.apps.ChatConfig",
    "Common.apps.CommonConfig",
    "Billing.apps.BillingConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PERSONAL_APPS

# ====================================
# MIDDLEWARE
# ====================================

DJANGO_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

THIRD_PARTY_MIDDLEWARE = []

PERSONAL_MIDDLEWARE = []

MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE + PERSONAL_MIDDLEWARE

# ====================================
# TEMPLATES
# ====================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ====================================
# SECURITY
# ====================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ====================================
# I18N
# ====================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ====================================
# LIBRARY - CORSHEADERS
# ====================================

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

# ====================================
# LIBRARY - DJANGO REST FRAMEWORK
# ====================================

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
    # PERMISSION
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    # SCHEMA
    "DEFAULT_SCHEMA_CLASS": "drf_standardized_errors.openapi.AutoSchema",
    # EXCEPTION
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    # FILTERING
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

# ====================================
# LIBRARY - SPECTACULAR
# ====================================

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

# ====================================
# LIBRARY - DJANGO PHONE NUMBER FIELD
# ====================================

PHONENUMBER_DEFAULT_REGION = "PE"

# ====================================
# LIBRARY - SIMPLE JSON WEB TOKENS
# ====================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "ON_LOGIN_SUCCESS": "rest_framework_simplejwt.serializers.default_on_login_success",
    "ON_LOGIN_FAILED": "rest_framework_simplejwt.serializers.default_on_login_failed",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
    "CHECK_REVOKE_TOKEN": False,
    "REVOKE_TOKEN_CLAIM": "hash_password",
    "CHECK_USER_IS_ACTIVE": True,
}
