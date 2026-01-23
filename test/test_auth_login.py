"""
Tests for the login endpoint.

This module tests the authentication login functionality including:
- Successful login with valid credentials
- Login failure with invalid credentials
- Rate limiting/throttling behavior
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


# =============================================================================
# Login Success Tests
# =============================================================================


def test_login_success(
    authenticated_client, url_login, valid_login_credentials, disable_all_throttles
):
    """
    Test successful login with valid credentials.

    Verifies that a user can log in successfully and receives
    both access_token and refresh_token cookies in the response.
    """
    response = authenticated_client.post(
        url_login, valid_login_credentials, format="json"
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


# =============================================================================
# Login Failure Tests
# =============================================================================


def test_login_invalid_credentials(
    authenticated_client, url_login, invalid_login_credentials, disable_all_throttles
):
    """
    Test login failure with invalid credentials.

    Verifies that login with wrong password returns 401 Unauthorized.
    """
    response = authenticated_client.post(
        url_login, invalid_login_credentials, format="json"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# Throttle Tests
# =============================================================================


def test_login_failed_attempts_throttle(
    authenticated_client, url_login, invalid_login_credentials, disable_auth_throttle
):
    """
    Test rate limiting after multiple failed login attempts.

    Verifies that after 3 failed login attempts (configured limit),
    subsequent requests are throttled with 429 Too Many Requests.

    Note: Only AuthRateThrottle is disabled to allow FailedLoginThrottle to work.
    The FailedLoginThrottle is configured with "3/30m" rate limit.
    """
    first_response = authenticated_client.post(
        url_login, invalid_login_credentials, format="json"
    )
    second_response = authenticated_client.post(
        url_login, invalid_login_credentials, format="json"
    )
    third_response = authenticated_client.post(
        url_login, invalid_login_credentials, format="json"
    )
    fourth_response = authenticated_client.post(
        url_login, invalid_login_credentials, format="json"
    )

    assert first_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert second_response.status_code == status.HTTP_401_UNAUTHORIZED
    assert third_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert fourth_response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
