DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
]

PERSONAL_APPS = [
    "apps.Authentication",
    "apps.Authorization",
    "apps.Chat",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PERSONAL_APPS
