from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIRS = os.path.join(BASE_DIR, "apps")
COMMONS_DIRS = os.path.join(BASE_DIR, "commons")
FIXTURES_DIRS = os.path.join(BASE_DIR, "fixtures")

if APPS_DIRS not in sys.path:
    sys.path.insert(0, APPS_DIRS)
if COMMONS_DIRS not in sys.path:
    sys.path.insert(0, COMMONS_DIRS)

ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True' 
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'