from django.urls import path

from .views import login, logout, refresh_token, register

app_name = "Authentication"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("refresh-token/", refresh_token, name="refresh_token"),
]
