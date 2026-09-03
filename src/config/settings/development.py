from .base import *

# ====================================
# BASIC CONFIG
# ====================================

DEBUG = os.environ.get("DEBUG", "True") == "True"

# ====================================
# DATABASES
# ====================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "CONN_MAX_AGE": 600,
        "OPTIONS": {
            "connect_timeout": 30,
            "keepalives": 1,
            "keepalives_idle": 30,
        },
    }
}

# ====================================
# CACHE
# ====================================

REDIS_USER = os.environ.get("REDIS_USER", "default")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_DB = os.environ.get("REDIS_DB", "0")

# Construct Redis URL with credentials
if REDIS_PASSWORD:
    REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# ====================================
# LIBRARY - CHANNELS
# ====================================

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # Explicitly disable the read timeout on the channel layer's
            # Redis connection. redis-py >=8.0.0 defaults socket_timeout to
            # 5s, which aborts RedisChannelLayer's blocking BZPOPMIN read
            # every ~5s of idle silence and kills the WebSocket consumer.
            # See https://github.com/django/channels_redis/issues/422
            "hosts": [
                {
                    "address": REDIS_URL,
                    "socket_timeout": None,
                    "socket_keepalive": True,
                    "health_check_interval": 15,
                    "retry_on_timeout": True,
                }
            ],
        },
    },
}

# ====================================
# CELERY RESULT
# ====================================

CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "default"
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_SERIALIZER = "json"

# ====================================
# CELERY
# ====================================

RABBITMQ_USER = os.environ.get("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_DEFAULT_PASS", "guest")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT", "5672")

CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# Route ML-heavy tasks to a dedicated queue so they never block
# lightweight tasks (e.g. agent responses).
CELERY_TASK_QUEUES_DEFAULT = "default"
CELERY_TASK_ROUTES = {
    "apps.MachineLearning.tasks.*": {"queue": "ml"},
}
CELERY_TASK_DEFAULT_QUEUE = "default"

# ====================================
# STATIC CONTENT
# ====================================

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfields")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafields")
