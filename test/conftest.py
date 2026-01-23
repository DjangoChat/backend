"""
Pytest configuration and fixtures for Platoform Backend tests.

This module provides shared fixtures for API testing, including:
- Database configuration
- API client instances
- Authentication helpers
- URL fixtures for Authentication endpoints
- Common test data (credentials, payloads)
- Throttle disabling fixtures
"""

from unittest.mock import patch

from django.conf import settings
from django.urls import reverse

import pytest

# =============================================================================
# Database Configuration
# =============================================================================


@pytest.fixture(scope="session")
def django_db_setup():
    """Configure test database settings."""
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }

    if not hasattr(settings, "DATABASES"):
        settings.DATABASES = {}

    for db_name in settings.DATABASES:
        settings.DATABASES[db_name]["ATOMIC_REQUESTS"] = True


# =============================================================================
# API Client Fixtures
# =============================================================================


@pytest.fixture
def api_client():
    """Return a DRF API client instance."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    """Return an authenticated API client with a test user."""
    user = django_user_model.objects.create_user(
        email="test@example.com", password="Testpassword123$"
    )
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_factory(django_user_model):
    """Factory fixture to create users with customizable attributes."""

    def create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "Testpassword123",
        }
        defaults.update(kwargs)
        return django_user_model.objects.create_user(**defaults)

    return create_user


# =============================================================================
# URL Fixtures for Authentication Endpoints
# =============================================================================


@pytest.fixture
def url_login():
    """Return the URL for the login endpoint."""
    return reverse("Authentication:login")


@pytest.fixture
def url_logout():
    """Return the URL for the logout endpoint."""
    return reverse("Authentication:logout")


@pytest.fixture
def url_register():
    """Return the URL for the registration endpoint."""
    return reverse("Authentication:register")


@pytest.fixture
def url_refresh_token():
    """Return the URL for the refresh token endpoint."""
    return reverse("Authentication:refresh_token")


# =============================================================================
# Common Test Data Fixtures
# =============================================================================


@pytest.fixture
def valid_login_credentials():
    """Return valid login credentials matching the authenticated_client user."""
    return {
        "email": "test@example.com",
        "password": "Testpassword123$",
    }


@pytest.fixture
def invalid_login_credentials():
    """Return invalid login credentials (wrong password)."""
    return {
        "email": "test@example.com",
        "password": "Testpassword124$",
    }


@pytest.fixture
def valid_registration_payload():
    """Return a valid registration payload."""
    return {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }


# =============================================================================
# Throttle Disabling Fixtures
# =============================================================================


@pytest.fixture
def disable_auth_throttle():
    """Disable AuthRateThrottle for tests that need it."""
    with patch(
        "apps.Authentication.api.v1.views.AuthView.AuthRateThrottle.allow_request",
        return_value=True,
    ):
        yield


@pytest.fixture
def disable_failed_login_throttle():
    """Disable FailedLoginThrottle for tests that need it."""
    with patch(
        "apps.Authentication.api.v1.views.AuthView.FailedLoginThrottle.allow_request",
        return_value=True,
    ):
        yield


@pytest.fixture
def disable_refresh_throttle():
    """Disable RefreshRateThrottle for tests that need it."""
    with patch(
        "apps.Authentication.api.v1.views.AuthView.RefreshRateThrottle.allow_request",
        return_value=True,
    ):
        yield


@pytest.fixture
def disable_all_throttles():
    """Disable all authentication-related throttles."""
    with (
        patch(
            "apps.Authentication.api.v1.views.AuthView.AuthRateThrottle.allow_request",
            return_value=True,
        ),
        patch(
            "apps.Authentication.api.v1.views.AuthView.FailedLoginThrottle.allow_request",
            return_value=True,
        ),
        patch(
            "apps.Authentication.api.v1.views.AuthView.RefreshRateThrottle.allow_request",
            return_value=True,
        ),
    ):
        yield
