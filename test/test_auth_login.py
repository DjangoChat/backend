from unittest.mock import patch

from django.urls import reverse

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


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


def test_login_bad_credentials(authenticated_client):
    url = reverse("Authentication:login")
    payload = {
        "email": "test@example.com",
        "password": "Testpassword124$",
    }
    response = authenticated_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
