from django.urls import path
from .views import login, logout, refresh_token

urlpatterns = [
    path("login/", login, name="authentication"),
    path("logout/", logout, name="authentication"),
    path("refresh-token/", refresh_token, name="authentication"),
]
