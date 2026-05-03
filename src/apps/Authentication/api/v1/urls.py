from django.urls import path

from .views import login, logout, refresh_token, register, me, UserProfileView

app_name = "Authentication"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("refresh-token/", refresh_token, name="refresh_token"),
    path("me/", me, name="me"),
    path(
        "profiles/",
        UserProfileView.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="profiles",
    ),
    path(
        "profiles/<uuid:pk>/",
        UserProfileView.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="profile",
    ),
]
