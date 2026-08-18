"""
Tests for the CookieJwtAuth authentication class.

This module tests the CookieJwtAuth authentication functionality including:
- Token extraction from cookies
- Token validation
- User retrieval from valid tokens
- Error handling for invalid tokens
- Handling missing tokens
"""

from unittest.mock import Mock, patch

import pytest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import (
    AuthenticationFailed as JWTAuthenticationFailed,
)
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.tokens import AccessToken

from apps.Authentication.authentication.CookieJwtAuth import CookieJwtAuth

pytestmark = pytest.mark.django_db


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def cookie_jwt_auth():
    """Return an instance of CookieJwtAuth."""
    return CookieJwtAuth()


@pytest.fixture
def mock_request():
    """Return a mock request object."""
    request = Mock()
    request.COOKIES = {}
    return request


@pytest.fixture
def test_user(django_user_model):
    """Create a test user for authentication."""
    return django_user_model.objects.create_user(
        email="testuser@example.com",
        password="TestPassword123!",
        phone="+12125551111",
    )


@pytest.fixture
def valid_access_token(test_user):
    """Generate a valid access token for the test user."""
    token = AccessToken.for_user(test_user)
    return str(token)


# =============================================================================
# Successful Authentication Tests
# =============================================================================


class TestCookieJwtAuthSuccess:
    """Test cases for successful authentication scenarios."""

    def test_authenticate_with_valid_token(
        self, cookie_jwt_auth, mock_request, test_user, valid_access_token
    ):
        """
        Test successful authentication with a valid access token in cookies.

        Verifies that a valid token in the access_token cookie returns
        the authenticated user and validated token.
        """
        mock_request.COOKIES["access_token"] = valid_access_token

        user, token = cookie_jwt_auth.authenticate(mock_request)

        assert user is not None
        assert user.id == test_user.id
        assert user.email == test_user.email
        assert token is not None

    def test_authenticate_returns_user_and_token_tuple(
        self, cookie_jwt_auth, mock_request, test_user, valid_access_token
    ):
        """
        Test that authenticate returns a tuple of (user, token).

        Verifies the return type matches DRF authentication expectations.
        """
        mock_request.COOKIES["access_token"] = valid_access_token

        result = cookie_jwt_auth.authenticate(mock_request)

        assert isinstance(result, tuple)
        assert len(result) == 2
        assert result[0] == test_user

    def test_authenticate_validates_token(
        self, cookie_jwt_auth, mock_request, test_user, valid_access_token
    ):
        """
        Test that authenticate validates the token before returning user.

        Verifies that token validation is performed.
        """
        mock_request.COOKIES["access_token"] = valid_access_token

        user, token = cookie_jwt_auth.authenticate(mock_request)

        # Token should be validated and contain expected claims
        assert "user_id" in token
        assert token["user_id"] == str(test_user.id)


# =============================================================================
# Missing Token Tests
# =============================================================================


class TestCookieJwtAuthMissingToken:
    """Test cases for handling missing tokens."""

    def test_authenticate_without_cookie_returns_none(
        self, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate returns None when no access_token cookie exists.

        Verifies that missing authentication credentials return None,
        allowing other authentication methods to be tried.
        """
        # No cookies set
        result = cookie_jwt_auth.authenticate(mock_request)

        assert result is None

    def test_authenticate_with_empty_token_returns_none(
        self, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate returns None when access_token cookie is empty.

        Verifies that empty token values are treated as missing.
        """
        mock_request.COOKIES["access_token"] = ""

        result = cookie_jwt_auth.authenticate(mock_request)

        assert result is None

    def test_authenticate_with_none_token_returns_none(
        self, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate returns None when access_token cookie is None.

        Verifies that None token values are treated as missing.
        """
        mock_request.COOKIES["access_token"] = None

        result = cookie_jwt_auth.authenticate(mock_request)

        assert result is None

    def test_authenticate_with_other_cookies_returns_none(
        self, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate returns None when only other cookies exist.

        Verifies that the method specifically looks for access_token cookie.
        """
        mock_request.COOKIES["other_cookie"] = "some_value"
        mock_request.COOKIES["session_id"] = "abc123"

        result = cookie_jwt_auth.authenticate(mock_request)

        assert result is None


# =============================================================================
# Invalid Token Tests
# =============================================================================


class TestCookieJwtAuthInvalidToken:
    """Test cases for handling invalid tokens."""

    def test_authenticate_with_invalid_token_raises_error(
        self, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate raises AuthenticationFailed for invalid tokens.

        Verifies that malformed or invalid tokens result in authentication failure.
        """
        mock_request.COOKIES["access_token"] = "invalid.token.here"

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        assert "Token validation failed" in str(exc_info.value)

    def test_authenticate_with_expired_token_raises_error(
        self, cookie_jwt_auth, mock_request, test_user
    ):
        """
        Test that authenticate raises AuthenticationFailed for expired tokens.

        Verifies that expired tokens are properly rejected.
        """
        # Create an expired token
        from datetime import timedelta

        from django.utils import timezone

        token = AccessToken.for_user(test_user)
        token.set_exp(lifetime=timedelta(seconds=-1))  # Already expired
        expired_token = str(token)

        mock_request.COOKIES["access_token"] = expired_token

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        assert "Token validation failed" in str(exc_info.value)

    def test_authenticate_with_malformed_token_raises_error(
        self, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate raises AuthenticationFailed for malformed tokens.

        Verifies that tokens with incorrect structure are rejected.
        """
        mock_request.COOKIES["access_token"] = "not-a-jwt-token"

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        assert "Token validation failed" in str(exc_info.value)

    def test_authenticate_with_tampered_token_raises_error(
        self, cookie_jwt_auth, mock_request, valid_access_token
    ):
        """
        Test that authenticate raises AuthenticationFailed for tampered tokens.

        Verifies that tokens with modified signatures are rejected.
        """
        # Tamper with the token by changing a character
        tampered_token = valid_access_token[:-5] + "XXXXX"
        mock_request.COOKIES["access_token"] = tampered_token

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        assert "Token validation failed" in str(exc_info.value)


# =============================================================================
# User Retrieval Error Tests
# =============================================================================


class TestCookieJwtAuthUserRetrievalErrors:
    """Test cases for errors during user retrieval."""

    def test_authenticate_with_nonexistent_user_raises_error(
        self, cookie_jwt_auth, mock_request, test_user, valid_access_token
    ):
        """
        Test that authenticate raises AuthenticationFailed when user doesn't exist.

        Verifies that tokens for deleted users are properly rejected.
        """
        mock_request.COOKIES["access_token"] = valid_access_token

        # Delete the user after creating the token
        test_user.delete()

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        assert "Error retrieving user" in str(exc_info.value)

    @patch.object(CookieJwtAuth, "get_user")
    def test_authenticate_handles_get_user_errors(
        self, mock_get_user, cookie_jwt_auth, mock_request, valid_access_token
    ):
        """
        Test that authenticate properly handles errors from get_user method.

        Verifies that exceptions during user retrieval are caught and wrapped.
        """
        mock_request.COOKIES["access_token"] = valid_access_token
        mock_get_user.side_effect = JWTAuthenticationFailed("User retrieval failed")

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        assert "Error retrieving user" in str(exc_info.value)


# =============================================================================
# Token Validation Tests
# =============================================================================


class TestCookieJwtAuthTokenValidation:
    """Test cases for token validation behavior."""

    @patch.object(CookieJwtAuth, "get_validated_token")
    def test_authenticate_calls_get_validated_token(
        self, mock_get_validated_token, cookie_jwt_auth, mock_request
    ):
        """
        Test that authenticate calls get_validated_token with the cookie token.

        Verifies that the token validation method is invoked.
        """
        mock_request.COOKIES["access_token"] = "some.token.here"
        mock_get_validated_token.side_effect = JWTAuthenticationFailed("Invalid")

        with pytest.raises(AuthenticationFailed):
            cookie_jwt_auth.authenticate(mock_request)

        mock_get_validated_token.assert_called_once_with("some.token.here")

    @patch.object(CookieJwtAuth, "get_validated_token")
    def test_authenticate_wraps_token_validation_errors(
        self, mock_get_validated_token, cookie_jwt_auth, mock_request
    ):
        """
        Test that token validation errors are wrapped with descriptive messages.

        Verifies that the error message includes context about validation failure.
        """
        mock_request.COOKIES["access_token"] = "invalid.token"
        mock_get_validated_token.side_effect = JWTAuthenticationFailed(
            "Token is invalid or expired"
        )

        with pytest.raises(AuthenticationFailed) as exc_info:
            cookie_jwt_auth.authenticate(mock_request)

        error_message = str(exc_info.value)
        assert "Token validation failed" in error_message
        assert "Token is invalid or expired" in error_message


# =============================================================================
# Integration Tests
# =============================================================================


class TestCookieJwtAuthIntegration:
    """Integration tests for CookieJwtAuth with real DRF views."""

    def test_authenticate_with_api_client(self, api_client, test_user):
        """
        Test authentication flow with DRF APIClient.

        Verifies that CookieJwtAuth works in a realistic request scenario.
        """
        # Generate a valid token
        token = AccessToken.for_user(test_user)
        access_token = str(token)

        # Set the cookie on the client
        api_client.cookies["access_token"] = access_token

        # Create a request and authenticate
        request = api_client.get("/").wsgi_request
        auth = CookieJwtAuth()

        user, validated_token = auth.authenticate(request)

        assert user.id == test_user.id
        assert validated_token is not None

    def test_multiple_authentication_attempts(
        self, cookie_jwt_auth, mock_request, test_user, valid_access_token
    ):
        """
        Test that the same auth instance can handle multiple requests.

        Verifies that the authentication class is stateless.
        """
        mock_request.COOKIES["access_token"] = valid_access_token

        # First authentication
        user1, token1 = cookie_jwt_auth.authenticate(mock_request)

        # Second authentication with same token
        user2, token2 = cookie_jwt_auth.authenticate(mock_request)

        assert user1.id == user2.id
        assert user1.id == test_user.id

    def test_authenticate_extracts_correct_cookie(
        self, cookie_jwt_auth, mock_request, test_user, valid_access_token
    ):
        """
        Test that authenticate extracts the correct cookie among multiple cookies.

        Verifies that only the access_token cookie is used for authentication.
        """
        mock_request.COOKIES["session_id"] = "abc123"
        mock_request.COOKIES["access_token"] = valid_access_token
        mock_request.COOKIES["refresh_token"] = "some.refresh.token"
        mock_request.COOKIES["other_data"] = "ignored"

        user, token = cookie_jwt_auth.authenticate(mock_request)

        assert user.id == test_user.id
        assert token is not None
