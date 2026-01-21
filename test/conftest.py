"""
Pytest configuration and fixtures for Platoform Backend tests.
"""

from django.conf import settings

import pytest


@pytest.fixture(scope="session")
def django_db_setup():
    """Configure test database settings."""
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }

    # Ensure ATOMIC_REQUESTS is set for the test environment
    if not hasattr(settings, "DATABASES"):
        settings.DATABASES = {}

    for db_name in settings.DATABASES:
        settings.DATABASES[db_name]["ATOMIC_REQUESTS"] = True


@pytest.fixture
def api_client():
    """Return a DRF API client instance."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    """Return an authenticated API client."""
    user = django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user_factory(django_user_model):
    """Factory fixture to create users."""

    def create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword123",
        }
        defaults.update(kwargs)
        return django_user_model.objects.create_user(**defaults)

    return create_user
