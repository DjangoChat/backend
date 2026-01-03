import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIRS = os.path.join(BASE_DIR, "apps")
FIXTURES_DIRS = os.path.join(BASE_DIR, "fixtures")

if APPS_DIRS not in sys.path:
    sys.path.insert(0, APPS_DIRS)

ENVIRONMENT = os.environ.get("ENV_TYPE", "development")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "Authentication.CustomUser"
