"""
Tests for the user registration endpoint.

This module tests the user registration functionality including:
- Successful registration with valid data
- Registration failures due to missing fields
- Registration failures due to password mismatch
- Registration failures due to duplicate email/phone
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


# =============================================================================
# Registration Success Tests
# =============================================================================


def test_register_success(
    api_client, url_register, valid_registration_payload, disable_auth_throttle
):
    """
    Test successful user registration.

    Verifies that a user can register successfully when providing
    valid email, phone, and matching passwords.
    """
    response = api_client.post(url_register, valid_registration_payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED


# =============================================================================
# Registration Missing Fields Tests
# =============================================================================


def test_register_missing_email(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to missing email.

    Verifies that the registration endpoint returns 400 Bad Request
    when the email field is missing from the payload.
    """
    payload = {
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url_register, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_missing_phone(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to missing phone number.

    Verifies that the registration endpoint returns 400 Bad Request
    when the phone field is missing from the payload.
    """
    payload = {
        "email": "newuser@example.com",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url_register, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_missing_password1(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to missing password1.

    Verifies that the registration endpoint returns 400 Bad Request
    when the password1 field is missing from the payload.
    """
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password2": "Strongpassword123$",
    }
    response = api_client.post(url_register, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_missing_password2(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to missing password2.

    Verifies that the registration endpoint returns 400 Bad Request
    when the password2 field is missing from the payload.
    """
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
    }
    response = api_client.post(url_register, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# =============================================================================
# Registration Password Validation Tests
# =============================================================================


def test_register_password_mismatch(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to password mismatch.

    Verifies that the registration endpoint returns 400 Bad Request
    when password1 and password2 do not match.
    """
    payload = {
        "email": "newuser@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword124$",
    }
    response = api_client.post(url_register, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


# =============================================================================
# Registration Duplicate Data Tests
# =============================================================================


def test_register_duplicate_phone(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to duplicate phone number.

    Verifies that the registration endpoint returns 400 Bad Request
    when the phone number is already associated with an existing account.
    """
    first_payload = {
        "email": "first@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    duplicate_payload = {
        "email": "second@example.com",
        "phone": "987654321",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }

    first_response = api_client.post(url_register, first_payload, format="json")
    duplicate_response = api_client.post(url_register, duplicate_payload, format="json")

    assert first_response.status_code == status.HTTP_201_CREATED
    assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST


def test_register_duplicate_email(api_client, url_register, disable_auth_throttle):
    """
    Test registration failure due to duplicate email.

    Verifies that the registration endpoint returns 400 Bad Request
    when the email is already associated with an existing account.
    """
    first_payload = {
        "email": "user@example.com",
        "phone": "987654322",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }
    duplicate_payload = {
        "email": "user@example.com",
        "phone": "987654323",
        "password1": "Strongpassword123$",
        "password2": "Strongpassword123$",
    }

    first_response = api_client.post(url_register, first_payload, format="json")
    duplicate_response = api_client.post(url_register, duplicate_payload, format="json")

    assert first_response.status_code == status.HTTP_201_CREATED
    assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST
