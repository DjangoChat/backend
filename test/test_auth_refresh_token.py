"""
Tests for the refresh token and logout endpoints.

This module tests the token refresh and logout functionality including:
- Successful token refresh
- Refresh failure with missing/invalid cookies
- Successful logout with cookie expiration
- Logout failure with missing refresh token
"""

import pytest
from rest_framework import status

pytestmark = pytest.mark.django_db


# =============================================================================
# Refresh Token Success Tests
# =============================================================================


def test_refresh_token_success(
    authenticated_client,
    url_login,
    url_refresh_token,
    valid_login_credentials,
    disable_all_throttles,
):
    """
    Test successful token refresh.

    Verifies that after login, the refresh endpoint issues a new
    access_token that differs from the original one.
    """
    login_response = authenticated_client.post(
        url_login, valid_login_credentials, format="json"
    )
    original_access_token = login_response.cookies.get("access_token")

    refresh_response = authenticated_client.post(url_refresh_token)

    assert refresh_response.status_code == status.HTTP_200_OK
    assert refresh_response.cookies.get("access_token") != original_access_token


# =============================================================================
# Refresh Token Failure Tests
# =============================================================================


def test_refresh_token_missing_cookie(
    api_client, url_refresh_token, disable_all_throttles
):
    """
    Test refresh failure when refresh_token cookie is missing.

    Verifies that the refresh endpoint returns 401 Unauthorized
    when no refresh_token cookie is present.
    """
    response = api_client.post(url_refresh_token)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token_invalid_cookie(
    authenticated_client, url_refresh_token, disable_all_throttles
):
    """
    Test refresh failure with an invalid refresh_token.

    Verifies that the refresh endpoint returns 401 Unauthorized
    when the refresh_token cookie contains an invalid token.
    """
    authenticated_client.cookies["refresh_token"] = "invalid_token_value"
    response = authenticated_client.post(url_refresh_token)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# =============================================================================
# Logout Success Tests
# =============================================================================


def test_logout_success(
    authenticated_client,
    url_login,
    url_logout,
    valid_login_credentials,
    disable_all_throttles,
):
    """
    Test successful logout.

    Verifies that after logout, both access_token and refresh_token
    cookies are expired (max-age set to 0).
    """
    authenticated_client.post(url_login, valid_login_credentials, format="json")

    logout_response = authenticated_client.post(url_logout)
    access_token_cookie = logout_response.cookies.get("access_token")
    refresh_token_cookie = logout_response.cookies.get("refresh_token")

    assert logout_response.status_code == status.HTTP_200_OK
    assert int(access_token_cookie["max-age"]) == 0
    assert int(refresh_token_cookie["max-age"]) == 0


# =============================================================================
# Logout Failure Tests
# =============================================================================


def test_logout_missing_refresh_token(
    authenticated_client, url_logout, disable_all_throttles
):
    """
    Test logout failure when refresh_token cookie is missing.

    Verifies that the logout endpoint returns 401 Unauthorized
    when no refresh_token cookie is present.
    """
    response = authenticated_client.post(url_logout)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
