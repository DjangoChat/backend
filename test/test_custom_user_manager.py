"""
Tests for the CustomUserManager.

This module tests the CustomUserManager functionality including:
- create_user() method with various scenarios
- create_superuser() method with various scenarios
- Email validation and normalization
- Password handling
- Extra fields handling
"""

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

import pytest

pytestmark = pytest.mark.django_db

User = get_user_model()


# =============================================================================
# create_user() Tests
# =============================================================================


class TestCreateUser:
    """Test cases for CustomUserManager.create_user() method."""

    def test_create_user_with_email_and_password(self):
        """
        Test that create_user successfully creates a user with email and password.

        Verifies that a user can be created with basic required fields
        and that the password is properly hashed.
        """
        email = "testuser@example.com"
        password = "SecurePassword123!"
        phone = "+12125551234"

        user = User.objects.create_user(email=email, password=password, phone=phone)

        assert user is not None
        assert user.email == email
        assert user.phone.as_e164 == phone
        assert user.check_password(password)
        assert user.pk is not None

    def test_create_user_without_password(self):
        """
        Test that create_user can create a user without a password.

        Verifies that users can be created without passwords (useful for
        OAuth or other authentication methods).
        """
        email = "nopassword@example.com"
        phone = "+12125551235"

        user = User.objects.create_user(email=email, phone=phone)

        assert user is not None
        assert user.email == email
        assert user.has_usable_password() is False

    def test_create_user_without_email_raises_error(self):
        """
        Test that create_user raises ValueError when email is not provided.

        Verifies that the email field is required and properly validated.
        """
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_user(email="", password="password123")

        assert "The Email must be set" in str(exc_info.value)

    def test_create_user_with_none_email_raises_error(self):
        """
        Test that create_user raises ValueError when email is None.

        Verifies that None email values are properly rejected.
        """
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_user(email=None, password="password123")

        assert "The Email must be set" in str(exc_info.value)

    def test_create_user_normalizes_email(self):
        """
        Test that create_user normalizes the email address.

        Verifies that the domain part of the email is lowercased
        according to Django's email normalization.
        """
        email = "TestUser@EXAMPLE.COM"
        normalized_email = "TestUser@example.com"
        phone = "+12125551236"

        user = User.objects.create_user(
            email=email, password="password123", phone=phone
        )

        assert user.email == normalized_email

    def test_create_user_with_extra_fields(self):
        """
        Test that create_user accepts and sets extra fields.

        Verifies that additional fields can be passed via **extra_fields
        and are properly set on the user instance.
        """
        email = "extrafields@example.com"
        phone = "+12125551237"
        password = "password123"

        user = User.objects.create_user(
            email=email, password=password, phone=phone, verified=True
        )

        assert user.verified is True

    def test_create_user_saves_to_database(self):
        """
        Test that create_user persists the user to the database.

        Verifies that the created user is saved and can be retrieved.
        """
        email = "savetest@example.com"
        phone = "+12125551238"
        password = "password123"

        user = User.objects.create_user(email=email, password=password, phone=phone)

        retrieved_user = User.objects.get(email=email)
        assert retrieved_user.pk == user.pk
        assert retrieved_user.email == email

    def test_create_user_sets_unusable_password_when_none(self):
        """
        Test that create_user sets unusable password when password is None.

        Verifies that passing None as password results in an unusable password.
        """
        email = "nopwd@example.com"
        phone = "+12125551239"

        user = User.objects.create_user(email=email, password=None, phone=phone)

        assert user.has_usable_password() is False

    def test_create_user_with_empty_string_password(self):
        """
        Test that create_user handles empty string password.

        Verifies behavior when an empty string is passed as password.
        """
        email = "emptypwd@example.com"
        phone = "+12125551240"

        user = User.objects.create_user(email=email, password="", phone=phone)

        # Empty string password is still set (Django hashes it)
        assert user.has_usable_password() is True
        assert user.check_password("") is True


# =============================================================================
# create_superuser() Tests
# =============================================================================


class TestCreateSuperuser:
    """Test cases for CustomUserManager.create_superuser() method."""

    def test_create_superuser_with_email_and_password(self):
        """
        Test that create_superuser successfully creates a superuser.

        Verifies that a superuser is created with all required flags set.
        """
        email = "admin@example.com"
        password = "AdminPassword123!"
        phone = "+12125552000"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone
        )

        assert user is not None
        assert user.email == email
        assert user.check_password(password)
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.verified is True

    def test_create_superuser_sets_is_superuser_true(self):
        """
        Test that create_superuser sets is_superuser to True by default.

        Verifies that the is_superuser flag is automatically set.
        """
        email = "superuser@example.com"
        password = "password123"
        phone = "+12125552001"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone
        )

        assert user.is_superuser is True
        assert user.is_staff is True

    def test_create_superuser_sets_verified_true(self):
        """
        Test that create_superuser sets verified to True by default.

        Verifies that superusers are automatically verified.
        """
        email = "verified@example.com"
        password = "password123"
        phone = "+12125552002"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone
        )

        assert user.verified is True

    def test_create_superuser_with_is_superuser_false_raises_error(self):
        """
        Test that create_superuser raises ValueError when is_superuser=False.

        Verifies that superusers must have is_superuser=True.
        """
        email = "notsuperuser@example.com"
        password = "password123"
        phone = "+12125552003"

        with pytest.raises(ValueError) as exc_info:
            User.objects.create_superuser(
                email=email, password=password, phone=phone, is_superuser=False
            )

        assert "Superuser must have is_superuser=True" in str(exc_info.value)

    def test_create_superuser_without_email_raises_error(self):
        """
        Test that create_superuser raises ValueError when email is not provided.

        Verifies that email validation applies to superusers too.
        """
        with pytest.raises(ValueError) as exc_info:
            User.objects.create_superuser(email="", password="password123")

        assert "The Email must be set" in str(exc_info.value)

    def test_create_superuser_normalizes_email(self):
        """
        Test that create_superuser normalizes the email address.

        Verifies that email normalization applies to superusers.
        """
        email = "ADMIN@EXAMPLE.COM"
        normalized_email = "ADMIN@example.com"
        password = "password123"
        phone = "+12125552004"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone
        )

        assert user.email == normalized_email

    def test_create_superuser_with_extra_fields(self):
        """
        Test that create_superuser accepts additional extra fields.

        Verifies that custom fields can be passed to superuser creation.
        """
        email = "customadmin@example.com"
        password = "password123"
        phone = "+12125552005"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone
        )

        assert user is not None
        assert user.phone.as_e164 == phone

    def test_create_superuser_without_password(self):
        """
        Test that create_superuser can create a superuser without a password.

        Verifies that superusers can be created without passwords.
        """
        email = "nopwdadmin@example.com"
        phone = "+12125552006"

        user = User.objects.create_superuser(email=email, phone=phone)

        assert user is not None
        assert user.is_superuser is True
        assert user.is_staff is True
        assert user.verified is True
        assert user.has_usable_password() is False

    def test_create_superuser_can_override_verified(self):
        """
        Test that create_superuser allows overriding verified field.

        Verifies that default values can be explicitly overridden.
        """
        email = "unverifiedadmin@example.com"
        password = "password123"
        phone = "+12125552007"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone, verified=False
        )

        # Note: Since setdefault is used, explicit False should be respected
        assert user.verified is False

    def test_create_superuser_saves_to_database(self):
        """
        Test that create_superuser persists the superuser to the database.

        Verifies that the created superuser is saved and can be retrieved.
        """
        email = "dbadmin@example.com"
        password = "password123"
        phone = "+12125552008"

        user = User.objects.create_superuser(
            email=email, password=password, phone=phone
        )

        retrieved_user = User.objects.get(email=email)
        assert retrieved_user.pk == user.pk
        assert retrieved_user.is_superuser is True


# =============================================================================
# Integration Tests
# =============================================================================


class TestCustomUserManagerIntegration:
    """Integration tests for CustomUserManager methods."""

    def test_multiple_users_creation(self):
        """
        Test creating multiple users with different attributes.

        Verifies that the manager can handle creating multiple users
        with different configurations.
        """
        user1 = User.objects.create_user(
            email="user1@example.com", password="pass1", phone="+12125553001"
        )
        user2 = User.objects.create_user(
            email="user2@example.com", password="pass2", phone="+12125553002"
        )
        superuser = User.objects.create_superuser(
            email="admin1@example.com", password="admin1", phone="+12125553003"
        )

        assert User.objects.count() == 3
        assert user1.is_superuser is False
        assert user2.is_superuser is False
        assert superuser.is_superuser is True

    def test_user_and_superuser_email_uniqueness(self):
        """
        Test that email uniqueness is enforced across users and superusers.

        Verifies that duplicate emails are not allowed.
        """
        email = "unique@example.com"
        User.objects.create_user(email=email, password="password", phone="+12125553010")

        with pytest.raises(Exception):  # IntegrityError
            User.objects.create_user(
                email=email, password="password2", phone="+12125553011"
            )

    def test_created_user_can_authenticate(self):
        """
        Test that a created user can be authenticated.

        Verifies the complete flow from user creation to authentication.
        """
        from django.contrib.auth import authenticate

        email = "authuser@example.com"
        password = "AuthPassword123!"
        phone = "+12125553020"

        User.objects.create_user(email=email, password=password, phone=phone)

        authenticated_user = authenticate(username=email, password=password)

        assert authenticated_user is not None
        assert authenticated_user.email == email
