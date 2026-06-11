from django.urls import path

from .views import OnboardingView, AuthenticationView

app_name = "Authentication"

urlpatterns = [
    path(
        "auth/login/",
        AuthenticationView.as_view({"post": "login"}),
    ),
    path(
        "auth/logut/",
        AuthenticationView.as_view({"post": "logout"}),
    ),
    path(
        "auth/refresh-token/",
        AuthenticationView.as_view({"post": "refresh_token"}),
    ),
    path(
        "auth/register/",
        AuthenticationView.as_view({"post": "register"}),
    ),
    path(
        "auth/me/",
        AuthenticationView.as_view({"post": "me"}),
    ),
    path(
        "onboardin/profile/",
        OnboardingView.as_view({"post": "create_profile_participant"}),
    ),
]
