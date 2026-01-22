from unittest.mock import patch

from django.urls import reverse

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def disable_throttling_globally():
    with patch(
        "apps.Authentication.api.v1.views.AuthView.AuthRateThrottle.allow_request",
        return_value=True,
    ):
        yield


def test_login_bad_credentials(authenticated_client):
    url = reverse("Authentication:login")
    payload = {
        "email": "test@example.com",
        "password": "Testpassword124$",
    }
    response = authenticated_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_success(authenticated_client):
    url = reverse("Authentication:login")
    payload = {
        "email": "test@example.com",
        "password": "Testpassword123$",
    }
    response = authenticated_client.post(url, payload, format="json")
    assert (
        response.status_code == status.HTTP_200_OK
        and "access_token" in response.cookies
        and "refresh_token" in response.cookies
    )


def test_login_personalize_throttle(authenticated_client):
    url = reverse("Authentication:login")
    payload = {
        "email": "test@example.com",
        "password": "Testpassword124$",
    }
    first_response = authenticated_client.post(url, payload, format="json")
    second_response = authenticated_client.post(url, payload, format="json")
    thrid_response = authenticated_client.post(url, payload, format="json")
    fourth_response = authenticated_client.post(url, payload, format="json")

    assert (
        first_response.status_code == status.HTTP_401_UNAUTHORIZED
        and second_response.status_code == status.HTTP_401_UNAUTHORIZED
        and thrid_response.status_code == status.HTTP_401_UNAUTHORIZED
        and fourth_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    )
