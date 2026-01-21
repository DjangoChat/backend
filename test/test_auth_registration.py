"""
Tests for the user registration endpoint.
"""

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


def test_registration_success(api_client):
    """
    Test successful user registration.

    This test ensures that a user can register successfully when providing
    valid email, phone, and matching passwords.
    """
    url = reverse("Authentication:register")
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED


def test_registration_missing_email(api_client):
    """
    Test registration failure due to missing email.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the email field is missing from the payload.
    """
    url = reverse("Authentication:register")
    payload = {
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_registration_missing_phone(api_client):
    """
    Test registration failure due to missing phone number.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the phone field is missing from the payload.
    """
    url = reverse("Authentication:register")
    payload = {
        "email": "newuser@example.com",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_registration_missing_password1(api_client):
    """
    Test registration failure due to missing password1.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the password1 field is missing from the payload.
    """
    url = reverse("Authentication:register")
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_registration_missing_password2(api_client):
    """
    Test registration failure due to missing password2.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the password2 field is missing from the payload.
    """
    url = reverse("Authentication:register")
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_registration_different_passwords(api_client):
    """
    Test registration failure due to different passwords.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the password1 and password2 fields do not match.
    """
    url = reverse("Authentication:register")
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword124$",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_registration_existing_phone(api_client):
    """
    Test registration failure due to existing phone number.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the phone number is already associated with an existing account.
    """
    url = reverse("Authentication:register")
    succesful_payload = {
        "email": "first@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    error_payload = {
        "email": "second@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    succesful_response = api_client.post(url, succesful_payload, format="json")
    error_response = api_client.post(url, error_payload, format="json")

    assert (
        succesful_response.status_code == status.HTTP_201_CREATED
        and error_response.status_code == status.HTTP_400_BAD_REQUEST
    )


def test_registration_existing_email(api_client):
    """
    Test registration failure due to existing email.

    This test ensures that the registration endpoint returns a 400 BAD REQUEST
    status when the email is already associated with an existing account.
    """
    url = reverse("Authentication:register")
    succesful_payload = {
        "email": "user@example.com",
        "phone": "987654322",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    error_payload = {
        "email": "user@example.com",
        "phone": "987654323",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    succesful_response = api_client.post(url, succesful_payload, format="json")
    error_response = api_client.post(url, error_payload, format="json")

    assert (
        succesful_response.status_code == status.HTTP_201_CREATED
        and error_response.status_code == status.HTTP_400_BAD_REQUEST
    )
