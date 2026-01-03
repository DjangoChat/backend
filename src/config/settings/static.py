import os

from .base import BASE_DIR

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "media"),
]

"""
static: handle by developers (html, css, js) content on a single file when python manage.py collecstatic
media: handle by users (images, files)
"""
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfields")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafields")
