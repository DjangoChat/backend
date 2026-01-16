from django.urls import path

from .views import hello, login, logout, refresh_token, register

urlpatterns = [
    path("login/", login, name="authentication"),
    path("logout/", logout, name="authentication"),
    path("register/", register, name="authentication"),
    path("refresh-token/", refresh_token, name="authentication"),
    path("hello/", hello, name="authentication"),
]
