from django.urls import path, include

from .views import OnboardingView, AuthenticationView

app_name = "Authentication"

urlpatterns = [
    path(
        "auth/",
        include(
            [
                path(
                    "login/",
                    AuthenticationView.as_view({"post": "login"}),
                ),
                path(
                    "logout/",
                    AuthenticationView.as_view({"post": "logout"}),
                ),
                path(
                    "refresh-token/",
                    AuthenticationView.as_view({"post": "refresh_token"}),
                ),
                path(
                    "register/",
                    AuthenticationView.as_view({"post": "register"}),
                ),
                path(
                    "me/",
                    AuthenticationView.as_view({"post": "me"}),
                ),
            ]
        ),
    ),
    path(
        "onboardin/profile/",
        OnboardingView.as_view({"post": "create_profile_participant"}),
    ),
]
